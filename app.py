import os
from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from db import get_conn
from auth import get_identity

load_dotenv()

app = Flask(__name__)

# -----------------------
# SECURITY CONFIG
# -----------------------
# Used by Flask to securely sign session cookies.
# The value should be provided through environment variables.
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# Check if the secret key environment variable is set
if not app.config["SECRET_KEY"]:
    raise ValueError("Environment variable 'SECRET_KEY' is not set")
else:
    print("SECRET_KEY is set")
print("APP FILE:", os.path.abspath(__file__))
print("TEMPLATE FOLDER:", app.template_folder)


# -----------------------
# HOME PAGE
# -----------------------
@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()

    # Channels
    cur.execute("SELECT id, name FROM channels")
    channels = cur.fetchall()

    # Threads
    cur.execute("""
        SELECT t.id, t.title, t.content, u.username, t.created_at
        FROM threads t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.id DESC
    """)
    threads = cur.fetchall()

    # Messages
    cur.execute("""
        SELECT m.id, m.content, u.username, c.name, m.created_at
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
        identity=get_identity()
    )


# -----------------------
# CREATE THREAD
# -----------------------
@app.route("/threads", methods=["POST"])
def create_thread():
    identity = get_identity()

    # Guests and registered users can create threads
    if identity == "logged_out":
        return "Not allowed (logged out)", 403

    title = request.form.get("title", "").strip()

    if not title:
        return "Thread title required", 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO threads (title, user_id)
        VALUES (%s, %s)
    """, (
        title,
        session["user_id"]
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")


# -----------------------
# SEND MESSAGE
# -----------------------
@app.route("/send", methods=["POST"])
def send():
    if "user_id" not in session:
        return "Not allowed (logged out)", 403

    content = request.form.get("content")

    if not content:
        return "Empty message not allowed", 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM channels WHERE name = 'general' LIMIT 1;")
    channel = cur.fetchone()

    if not channel:
        return "Channel not found", 500

    cur.execute("""
        INSERT INTO messages (channel_id, author_id, content)
        VALUES (%s, %s, %s)
    """, (channel[0], session["user_id"], content))

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")


# -----------------------
# GUEST LOGIN
# -----------------------
@app.route("/guest-login")
def guest_login():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = 'guest' LIMIT 1;")
    user = cur.fetchone()

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
    username = request.form.get("username")

    if not username:
        return "Username required", 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, username FROM users WHERE username = %s;", (username,))
    user = cur.fetchone()

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
    session.clear()
    return redirect("/")


# -----------------------
# RUN
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)