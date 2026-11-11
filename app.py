"""
DEBRIS CAREERS — Main Flask Web Application
Premium Minimal AI Career Consultant Platform
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import os
import urllib.request
import json
import database as db
from rule_engine import CareerRuleEngine

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize SQLite database on startup
db.init_db()

def get_current_user():
    """Retrieve logged-in user info from session."""
    user_id = session.get("user_id")
    email = session.get("user_email")
    if user_id and email:
        return {"id": user_id, "email": email}
    return None

def query_ollama_if_available(prompt: str, system_context: str = ""):
    """
    Checks if Ollama is running locally at localhost:11434.
    If available, queries Ollama model; otherwise returns None to fallback to CareerRuleEngine.
    """
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3",
            "prompt": f"{system_context}\n\nUser Question: {prompt}\nAnswer:",
            "stream": False
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response")
    except Exception:
        # Ollama not running or model not found, seamlessly fallback to built-in NLP engine
        pass
    return None

# ============================================================================
# Core Chatbot Routes
# ============================================================================

@app.route("/")
def index():
    """Root route: Redirect to login or load latest conversation."""
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_view"))
    
    convs = db.get_user_conversations(user["id"])
    if not convs:
        conv_id = db.create_conversation(user["id"], "New Consultation")
        return redirect(url_for("chat_view", conv_id=conv_id))
    
    return redirect(url_for("chat_view", conv_id=convs[0]["id"]))

@app.route("/chat/<conv_id>")
def chat_view(conv_id):
    """View a specific consultation conversation."""
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_view"))
    
    messages = db.get_conversation_messages(conv_id, user["id"])
    if messages is None:
        return redirect(url_for("index"))
    
    convs = db.get_user_conversations(user["id"])
    current_conv = next((c for c in convs if c["id"] == conv_id), None)

    return render_template(
        "index.html",
        conversations=convs,
        current_conversation=current_conv,
        active_conv_id=conv_id,
        messages=messages,
        user_email=user["email"]
    )

@app.route("/chat/new")
def new_conversation():
    """Start a fresh consultation session."""
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_view"))

    conv_id = db.create_conversation(user["id"], "New Consultation")
    return redirect(url_for("chat_view", conv_id=conv_id))

@app.route("/chat/delete/<conv_id>", methods=["POST"])
def delete_chat(conv_id):
    """Permanently delete a specific chat conversation."""
    user = get_current_user()
    if not user:
        if request.is_json:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        return redirect(url_for("auth_view"))
    
    deleted = db.delete_conversation(conv_id, user["id"])
    
    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status": "success", "deleted": deleted, "conv_id": conv_id})
    
    return redirect(url_for("index"))

@app.route("/chat/clear_all", methods=["POST"])
def clear_all_chats():
    """Clear all chat history for current user."""
    user = get_current_user()
    if not user:
        if request.is_json:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        return redirect(url_for("auth_view"))
    
    db.clear_all_conversations(user["id"])
    
    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status": "success"})
    
    return redirect(url_for("index"))

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Process user message and return AI response."""
    user = get_current_user()
    if not user:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    data = request.get_json() or {}
    conv_id = data.get("conversation_id")
    user_msg = (data.get("message") or "").strip()

    if not conv_id or not user_msg:
        return jsonify({"status": "error", "message": "Missing conversation ID or message"}), 400

    # Verify conversation ownership
    existing_messages = db.get_conversation_messages(conv_id, user["id"])
    if existing_messages is None:
        return jsonify({"status": "error", "message": "Conversation not found"}), 404

    # Save user message to database
    user_time = db.save_message(conv_id, "user", user_msg)

    # If first user message, generate concise conversation title
    user_messages_count = sum(1 for m in existing_messages if m["sender"] == "user")
    if user_messages_count == 0:
        clean_title = user_msg[:28] + ("..." if len(user_msg) > 28 else "")
        db.update_conversation_title(conv_id, clean_title)

    # Retrieve conversation context state
    state = db.get_conversation_state(conv_id)

    # Check if Ollama is available, otherwise use NLP Rule Engine
    ollama_reply = query_ollama_if_available(user_msg, system_context="You are Debris Careers AI, an expert academic and career counselor.")
    if ollama_reply:
        bot_reply = ollama_reply
        updated_state = state
        options = []
    else:
        bot_reply, updated_state, options = CareerRuleEngine.process_message(user_msg, state)

    # Save updated context state
    db.save_conversation_state(conv_id, updated_state)

    # Save bot response to database
    bot_time = db.save_message(conv_id, "bot", bot_reply, options)

    return jsonify({
        "status": "success",
        "bot_message": bot_reply,
        "user_time": user_time,
        "bot_time": bot_time
    })

# ============================================================================
# Authentication Routes
# ============================================================================

@app.route("/auth")
def auth_view():
    """Display Login & Sign-up page."""
    if get_current_user():
        return redirect(url_for("index"))
    return render_template("auth.html", mode=request.args.get("mode", "login"))

@app.route("/auth/login", methods=["POST"])
def auth_login():
    """Handle user login with email and password validation."""
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("auth.html", error="Please provide both email and password.", mode="login")

    success, result = db.verify_user(email, password)
    if success:
        session["user_id"] = result["id"]
        session["user_email"] = result["email"]
        return redirect(url_for("index"))
    else:
        return render_template("auth.html", error=result, mode="login")

@app.route("/auth/register", methods=["POST"])
def auth_register():
    """Handle user registration."""
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("auth.html", error="Please provide both email and password.", mode="register")

    success, result = db.register_user(email, password)
    if success:
        session["user_id"] = result["id"]
        session["user_email"] = result["email"]
        return redirect(url_for("index"))
    else:
        return render_template("auth.html", error=result, mode="register")

@app.route("/auth/logout")
def auth_logout():
    """Clear session and securely log out."""
    session.clear()
    return redirect(url_for("auth_view"))

# ============================================================================
# Presentation Deck Routes (Microsoft Innovate 2026)
# ============================================================================

@app.route("/presentation")
def presentation_view():
    """Interactive Microsoft Innovate 2026 Presentation Viewer"""
    return render_template("presentation.html")

@app.route("/presentation/download")
def presentation_download():
    """Direct download of the official Microsoft Innovate 2026 PDF Presentation"""
    pdf_path = os.path.join(app.root_path, "Debris_Careers_Microsoft_Innovate_2026_Presentation.pdf")
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name="Debris_Careers_Microsoft_Innovate_2026_Presentation.pdf")
    return "Presentation PDF not found. Run generate_presentation_pdf.py first.", 404

# ============================================================================
# Server Port Configuration
# ============================================================================

def find_available_port(default_port=5005):
    """Find a guaranteed free port starting from default_port, avoiding macOS system conflicts."""
    import socket
    for p in range(default_port, default_port + 30):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', p)) != 0:
                return p
    return default_port

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        target_port = int(sys.argv[1])
    else:
        target_port = find_available_port(default_port=5005)

    print("=" * 65)
    print("✨  DEBRIS CAREERS — AI & NLP CAREER CONSULTANT PLATFORM")
    print(f"🚀  Server running live at:")
    print(f"👉  http://127.0.0.1:{target_port}")
    print("=" * 65)
    app.run(host="127.0.0.1", port=target_port, debug=False)
