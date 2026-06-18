 import os
from flask import Flask, render_template, request, redirect, session, jsonify

from db import get_conn
from auth import get_identity

app = Flask(__name__)

# =====================================================
# CONFIG (RAILWAY POSTGRES SAFE)
# =====================================================
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-this"
)


# =====================================================
# HOME PAGE
# =====================================================
@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()

    # Channels
    cur.execute("SELECT id, name FROM channels")
    channels = cur.fetchall()

    # Threads
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

    # Messages (global chat)
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
        user_id=session.get("user_id"),
        identity=get_identity()
    )


# =====================================================
# CREATE THREAD
# =====================================================
@app.route("/threads", methods=["POST"])
def create_thread():
    if "user_id" not in session:
        return "Not allowed (logged out)", 403

    title = request.form.get("title")
    content = request.form.get("content")

    if not title or not content:
        return "Title and content required", 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO threads (title, content, user_id)
        VALUES (%s, %s, %s)
    """, (title, content, session["user_id"]))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


# =====================================================
# VIEW THREAD PAGE
# =====================================================
@app.route("/threads/<int:thread_id>")
def view_thread(thread_id):
    conn = get_conn()
    cur = conn.cursor()

    # Thread
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

    if not thread:
        cur.close()
        conn.close()
        return "Thread not found", 404

    cur.close()
    conn.close()

    return render_template(
        "thread.html",
        thread=thread,
        user=session.get("username"),
        user_id=session.get("user_id"),
        identity=get_identity()
    )


# =====================================================
# CREATE REPLY (POSTGRES + API STYLE FIX)
# =====================================================
@app.route("/replies", methods=["POST"])
def create_reply():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    content = request.form.get("content")
    thread_id = request.form.get("thread_id")

    if not content or not thread_id:
        return jsonify({"error": "Missing data"}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO replies (thread_id, user_id, content)
        VALUES (%s, %s, %s)
    """, (thread_id, session["user_id"], content))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"success": True})


# =====================================================
# GET REPLIES API (CONVERSATION SYSTEM)
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
# CHANNEL CHAT SYSTEM
# =====================================================
@app.route("/send", methods=["POST"])
def send():
    if "user_id" not in session:
        return "Not allowed (logged out)", 403

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
    """, (channel[0], session["user_id"], content))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


# =====================================================
# GUEST LOGIN
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

    if not user:
        cur.close()
        conn.close()
        return "Guest user not found", 500

    session["user_id"] = user[0]
    session["username"] = user[1]

    cur.close()
    conn.close()

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

    if not user:
        cur.close()
        conn.close()
        return "User not found", 404

    session["user_id"] = user[0]
    session["username"] = user[1]

    cur.close()
    conn.close()

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