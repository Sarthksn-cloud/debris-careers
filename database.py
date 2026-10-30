import sqlite3
import hashlib
import uuid
from datetime import datetime
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debris_careers.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with a salt."""
    salt = "debris_careers_salt_"
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

def init_db():
    """Initialize database tables for users, conversations, and messages."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # User table with email and password (enforcing max 8 chars at application layer)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Conversations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        state_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );
    """)

    # Messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT NOT NULL,
        sender TEXT NOT NULL,
        content TEXT NOT NULL,
        options TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

def register_user(email: str, password: str):
    """
    Register a user with an email and password.
    Validation: Password must be maximum 8 characters.
    """
    email = email.strip().lower()
    if not email or "@" not in email:
        return False, "Please enter a valid email address."
    
    if len(password) < 1:
        return False, "Password cannot be empty."
    
    if len(password) > 8:
        return False, "Security constraint: Password must be maximum 8 characters."

    pwd_hash = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, pwd_hash))
        conn.commit()
        user_id = cursor.lastrowid
        return True, {"id": user_id, "email": email}
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    finally:
        conn.close()

def verify_user(email: str, password: str):
    """Verify login credentials."""
    email = email.strip().lower()
    pwd_hash = hash_password(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, password_hash FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and user["password_hash"] == pwd_hash:
        return True, {"id": user["id"], "email": user["email"]}
    return False, "Invalid email or password."

def create_conversation(user_id: int, initial_title: str = "New Consultation"):
    """Create a new chat conversation for a user."""
    conv_id = str(uuid.uuid4())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (id, user_id, title, state_data)
        VALUES (?, ?, ?, ?)
    """, (conv_id, user_id, initial_title, json.dumps({})))
    conn.commit()
    conn.close()
    return conv_id

def get_user_conversations(user_id: int):
    """Get all past conversations for the user sorted by latest first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, created_at, updated_at 
        FROM conversations 
        WHERE user_id = ? 
        ORDER BY updated_at DESC
    """, (user_id,))
    convs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return convs

def get_conversation_messages(conv_id: str, user_id: int):
    """Fetch all messages for a specific conversation belonging to the user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check ownership
    cursor.execute("SELECT id FROM conversations WHERE id = ? AND user_id = ?", (conv_id, user_id))
    if not cursor.fetchone():
        conn.close()
        return None

    cursor.execute("""
        SELECT id, sender, content, options, timestamp 
        FROM messages 
        WHERE conversation_id = ? 
        ORDER BY id ASC
    """, (conv_id,))
    messages = []
    for row in cursor.fetchall():
        msg = dict(row)
        if msg["options"]:
            try:
                msg["options"] = json.loads(msg["options"])
            except Exception:
                msg["options"] = []
        else:
            msg["options"] = []
        messages.append(msg)
    conn.close()
    return messages

def save_message(conv_id: str, sender: str, content: str, options: list = None):
    """Save a user or bot message and update conversation timestamp."""
    conn = get_db_connection()
    cursor = conn.cursor()
    options_json = json.dumps(options) if options else None
    cursor.execute("""
        INSERT INTO messages (conversation_id, sender, content, options)
        VALUES (?, ?, ?, ?)
    """, (conv_id, sender, content, options_json))
    
    # Update conversation's updated_at timestamp
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conv_id))
    
    conn.commit()
    conn.close()

def update_conversation_title(conv_id: str, title: str):
    """Update title of a conversation based on the user's first query."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE conversations SET title = ? WHERE id = ?", (title[:30], conv_id))
    conn.commit()
    conn.close()

def get_conversation_state(conv_id: str):
    """Retrieve the rule-engine state for this conversation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT state_data FROM conversations WHERE id = ?", (conv_id,))
    row = cursor.fetchone()
    conn.close()
    if row and row["state_data"]:
        try:
            return json.loads(row["state_data"])
        except Exception:
            return {}
    return {}

def save_conversation_state(conv_id: str, state: dict):
    """Persist the rule-engine state for this conversation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE conversations SET state_data = ? WHERE id = ?", (json.dumps(state), conv_id))
    conn.commit()
    conn.close()

def delete_conversation(conv_id: str, user_id: int):
    """Delete a specific conversation and all its messages."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Ensure user owns this conversation
    cursor.execute("DELETE FROM messages WHERE conversation_id = ? AND conversation_id IN (SELECT id FROM conversations WHERE user_id = ?)", (conv_id, user_id))
    cursor.execute("DELETE FROM conversations WHERE id = ? AND user_id = ?", (conv_id, user_id))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

def clear_all_conversations(user_id: int):
    """Delete all conversations and messages for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE conversation_id IN (SELECT id FROM conversations WHERE user_id = ?)", (user_id,))
    cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    init_db()
    print("Debris Careers Database initialized successfully at:", DB_PATH)
