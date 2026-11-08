"""
Debris Careers - Main Flask Web Application
Rule-based Career Consultant with Minimalist Monochrome Design.
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os
import re
import database as db
from rule_engine import CareerRuleEngine

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize the SQLite database on startup
db.init_db()

def get_current_user():
    """Retrieve logged-in user info from session."""
    user_id = session.get("user_id")
    email = session.get("user_email")
    if user_id and email:
        return {"id": user_id, "email": email}
    return None

@app.route("/")
def index():
    """Root route: Redirect to login or load the latest conversation."""
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_view"))
    
    # Retrieve user's conversations
    convs = db.get_user_conversations(user["id"])
    if not convs:
        # Create initial conversation (clean start, wait for user input)
        conv_id = db.create_conversation(user["id"], "New Consultation")
        return redirect(url_for("chat_view", conv_id=conv_id))
    
    # Redirect to most recently updated conversation
    return redirect(url_for("chat_view", conv_id=convs[0]["id"]))

@app.route("/chat/<conv_id>")
def chat_view(conv_id):
    """View a specific consultation conversation."""
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_view"))
    
    messages = db.get_conversation_messages(conv_id, user["id"])
    if messages is None:
        # User doesn't own this conversation or it doesn't exist
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
    """Create a new consultation session waiting for user input."""
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_view"))

    conv_id = db.create_conversation(user["id"], "New Consultation")
    return redirect(url_for("chat_view", conv_id=conv_id))

@app.route("/chat/delete/<conv_id>", methods=["POST"])
def delete_chat(conv_id):
    """Delete a specific chat conversation."""
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_view"))
    
    db.delete_conversation(conv_id, user["id"])
    return redirect(url_for("index"))

@app.route("/chat/clear_all", methods=["POST"])
def clear_all_chats():
    """Clear all chat history for current user."""
    user = get_current_user()
    if not user:
        return redirect(url_for("auth_view"))
    
    db.clear_all_conversations(user["id"])
    return redirect(url_for("index"))

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Process user message using the Rule-Based Consultant Engine."""
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
    db.save_message(conv_id, "user", user_msg)

    # If this is the user's first message, update conversation title
    user_messages_count = sum(1 for m in existing_messages if m["sender"] == "user")
    if user_messages_count == 0:
        clean_title = user_msg[:28] + ("..." if len(user_msg) > 28 else "")
        db.update_conversation_title(conv_id, clean_title)

    # Retrieve conversational state for this session
    state = db.get_conversation_state(conv_id)

    # Process message through Rule Engine (Deterministic, No API)
    bot_reply, updated_state, options = CareerRuleEngine.process_message(user_msg, state)

    # Save updated state
    db.save_conversation_state(conv_id, updated_state)

    # Save bot message to database
    db.save_message(conv_id, "bot", bot_reply, options)

    return jsonify({
        "status": "success",
        "bot_message": bot_reply,
        "options": options
    })

# Authentication Views
@app.route("/auth")
def auth_view():
    """Display Login & Registration forms."""
    if get_current_user():
        return redirect(url_for("index"))
    return render_template("auth.html", mode=request.args.get("mode", "login"))

@app.route("/auth/login", methods=["POST"])
def auth_login():
    """Handle user login."""
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if len(password) > 8:
        return render_template("auth.html", error="Password policy: Maximum 8 characters allowed.", mode="login")

    success, result = db.verify_user(email, password)
    if success:
        session["user_id"] = result["id"]
        session["user_email"] = result["email"]
        return redirect(url_for("index"))
    else:
        return render_template("auth.html", error=result, mode="login")

@app.route("/auth/register", methods=["POST"])
def auth_register():
    """Handle new user registration with strict 8-char password limit."""
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if len(password) > 8:
        return render_template("auth.html", error="Password policy: Password must be maximum 8 characters.", mode="register")
    
    if len(password) < 1:
        return render_template("auth.html", error="Password cannot be empty.", mode="register")

    success, result = db.register_user(email, password)
    if success:
        session["user_id"] = result["id"]
        session["user_email"] = result["email"]
        return redirect(url_for("index"))
    else:
        return render_template("auth.html", error=result, mode="register")

@app.route("/auth/logout")
def auth_logout():
    """Clear session and log out user."""
    session.clear()
    return redirect(url_for("auth_view"))

if __name__ == "__main__":
    print("=" * 60)
    print("🏛️ Debris Careers — Expert Rule-Based Consultant Web Server")
    print("Minimalist Black & White UI | Deterministic Expert System")
    print("Running at: http://127.0.0.1:5001")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5001, debug=True)
