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
