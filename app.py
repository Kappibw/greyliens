from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
import os

from db import get_conn
from auth import get_identity

# Load environment variables
load_dotenv()

app = Flask(__name__)


# -----------------------
# SECURITY CONFIG
# -----------------------

# Flask uses SECRET_KEY to securely sign session cookies.
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise ValueError("Environment variable 'SECRET_KEY' is not set")


# -----------------------
# HOME PAGE
# -----------------------

@app.route("/")
def index():
    """
    Displays the forum homepage.

    Retrieves messages from PostgreSQL and sends them
    to the forum template.
    """

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            m.id,
            m.content,
            u.username,
            c.name,
            m.created_at
        FROM messages m
        JOIN users u
            ON m.user_id = u.id
        JOIN channels c
            ON m.channel_id = c.id
        ORDER BY m.id DESC;
    """)

    messages = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "forum.html",
        messages=messages,
        user=session.get("username"),
        identity=get_identity()
    )


# -----------------------
# SEND MESSAGE
# -----------------------

@app.route("/send", methods=["POST"])
def send():
    """
    Creates a new message.

    Only logged-in users can send messages.
    """

    if "user_id" not in session:
        return "Not allowed (logged out)", 403

    content = request.form.get("content", "").strip()

    if not content:
        return "Empty message not allowed", 400

    conn = get_conn()
    cur = conn.cursor()

    # Use the first available channel for MVP posting
    cur.execute("""
        SELECT id
        FROM channels
        LIMIT 1;
    """)

    channel = cur.fetchone()

    if not channel:
        cur.close()
        conn.close()
        return "No channel found", 500

    cur.execute("""
        INSERT INTO messages
        (user_id, channel_id, content)
        VALUES (%s, %s, %s);
    """, (
        session["user_id"],
        channel[0],
        content
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")


# -----------------------
# GUEST LOGIN
# -----------------------

@app.route("/guest-login")
def guest_login():
    """
    Logs in using the guest account.
    """

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM users
        WHERE username = 'guest'
        LIMIT 1;
    """)

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return "Guest user not found", 500

    session["user_id"] = user[0]
    session["username"] = "guest"

    return redirect("/")


# -----------------------
# LOGIN
# -----------------------

@app.route("/login", methods=["POST"])
def login():
    """
    Logs in a user using username.
    """

    username = request.form.get("username", "").strip()

    if not username:
        return "Username required", 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username
        FROM users
        WHERE username = %s;
    """, (username,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return "User not found", 404

    session["user_id"] = user[0]
    session["username"] = user[1]

    return redirect("/")


# -----------------------
# LOGOUT
# -----------------------

@app.route("/logout")
def logout():
    """
    Clears the current user's session.
    """

    session.clear()

    return redirect("/")


# -----------------------
# RUN APP
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask, render_template, request, redirect, session, jsonify

from db import get_conn
from auth import get_identity

app = Flask(__name__)

# =====================================================
# CONFIG
# =====================================================
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-this"
)


# =====================================================
# AUTH HELPER
# =====================================================
def require_login():
    return session.get("user_id") is not None


def current_user():
    return session.get("user_id")


# =====================================================
# HOME PAGE
# =====================================================
@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM channels")
    channels = cur.fetchall()

    cur.execute("""
        SELECT
            t.id,
            t.title,
            t.content,
            u.username,
            t.created_at
        FROM threads t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.id DESC
    """)
    threads = cur.fetchall()

    cur.execute("""
        SELECT
            m.id,
            m.content,
            u.username,
            c.name,
            m.created_at
        FROM messages m
        JOIN users u ON m.author_id = u.id
        JOIN channels c ON m.channel_id = c.id
        ORDER BY m.id DESC
    """)
    messages = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "forum.html",
        channels=channels,
        threads=threads,
        messages=messages,
        user=session.get("username"),
        user_id=current_user(),
        identity=get_identity()
    )


# =====================================================
# CREATE THREAD
# =====================================================
@app.route("/threads", methods=["POST"])
def create_thread():
    if not require_login():
        return jsonify({"error": "Unauthorized"}), 403

    title = request.form.get("title")
    content = request.form.get("content")

    if not title or not content:
        return jsonify({"error": "Title and content required"}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO threads (title, content, user_id)
        VALUES (%s, %s, %s)
    """, (title, content, current_user()))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


# =====================================================
# VIEW THREAD
# =====================================================
@app.route("/threads/<int:thread_id>")
def view_thread(thread_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            t.id,
            t.title,
            t.content,
            u.username,
            t.created_at
        FROM threads t
        JOIN users u ON t.user_id = u.id
        WHERE t.id = %s
    """, (thread_id,))

    thread = cur.fetchone()

    cur.close()
    conn.close()

    if not thread:
        return "Thread not found", 404

    return render_template(
        "thread.html",
        thread=thread,
        user=session.get("username"),
        user_id=current_user(),
        identity=get_identity()
    )


# =====================================================
# CREATE REPLY
# =====================================================
@app.route("/replies", methods=["POST"])
def create_reply():
    if not require_login():
        return jsonify({"error": "Unauthorized"}), 401

    content = request.form.get("content")
    thread_id = request.form.get("thread_id")

    if not content or not thread_id:
        return jsonify({"error": "Missing data"}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO replies (thread_id, user_id, content)
        VALUES (%s, %s, %s)
    """, (thread_id, current_user(), content))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"success": True})


# =====================================================
# GET REPLIES
# =====================================================
@app.route("/api/replies/<int:thread_id>")
def get_replies(thread_id):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            r.id,
            r.content,
            u.username,
            r.created_at
        FROM replies r
        JOIN users u ON r.user_id = u.id
        WHERE r.thread_id = %s
        ORDER BY r.id ASC
    """, (thread_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {
            "id": r[0],
            "content": r[1],
            "username": r[2],
            "created_at": str(r[3])
        }
        for r in rows
    ])


# =====================================================
# SEND MESSAGE
# =====================================================
@app.route("/send", methods=["POST"])
def send():
    if not require_login():
        return "Unauthorized", 403

    content = request.form.get("content")

    if not content:
        return "Empty message not allowed", 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM channels WHERE name = 'general' LIMIT 1
    """)
    channel = cur.fetchone()

    if not channel:
        cur.close()
        conn.close()
        return "Channel not found", 500

    cur.execute("""
        INSERT INTO messages (channel_id, author_id, content)
        VALUES (%s, %s, %s)
    """, (channel[0], current_user(), content))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


# =====================================================
# GUEST LOGIN (SAFER)
# =====================================================
@app.route("/guest-login")
def guest_login():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username
        FROM users
        WHERE username = 'guest'
        LIMIT 1
    """)
    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return "Guest account not found", 500

    session["user_id"] = user[0]
    session["username"] = user[1]

    return redirect("/")


# =====================================================
# LOGIN
# =====================================================
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")

    if not username:
        return "Username required", 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username
        FROM users
        WHERE username = %s
    """, (username,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return "User not found", 404

    session["user_id"] = user[0]
    session["username"] = user[1]

    return redirect("/")


# =====================================================
# LOGOUT
# =====================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =====================================================
# RUN SERVER
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)