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

    Retrieves channels and replies (messages) together with their
    authors and channel metadata, then renders the forum page.
    """

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name
        FROM channels
        ORDER BY id;
    """)
    channels = cur.fetchall()

    cur.execute("""
        SELECT
            m.id,
            m.content,
            u.username,
            m.created_at
        FROM messages m
        JOIN users u
            ON m.user_id = u.id
        ORDER BY m.id DESC;
    """)
    replies = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "forum.html",
        channels=channels,
        replies=replies,
        user=session.get("username"),
        identity=get_identity(),
    )


# -----------------------
# SEND MESSAGE
# -----------------------

@app.route("/send", methods=["POST"])
def send():
    """
    Creates a new message in the general channel.

    Only authenticated users are allowed to submit messages.
    """

    if "user_id" not in session:
        return "Not allowed (logged out)", 403

    content = request.form.get("content", "").strip()

    if not content:
        return "Empty message not allowed", 400

    conn = get_conn()
    cur = conn.cursor()

    user_id = session["user_id"]

    cur.execute("""
        SELECT id
        FROM channels
        WHERE name = 'general'
        LIMIT 1;
    """)
    channel = cur.fetchone()

    if not channel:
        cur.execute("""
            INSERT INTO channels (name)
            VALUES (%s)
            RETURNING id;
        """, ("general",))
        created = cur.fetchone()
        if not created:
            cur.close()
            conn.close()
            return "Failed to create channel", 500
        channel_id = created[0]
        conn.commit()
    else:
        channel_id = channel[0]

    cur.execute("""
        INSERT INTO messages (channel_id, user_id, content)
        VALUES (%s, %s, %s)
    """, (channel_id, user_id, content))

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
    Logs a user into the application using the guest account.
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

    if not user:
        cur.execute("""
            INSERT INTO users (username)
            VALUES (%s)
            RETURNING id;
        """, ("guest",))
        created = cur.fetchone()
        if not created:
            cur.close()
            conn.close()
            return "Failed to create guest user", 500
        user_id = created[0]
        conn.commit()
    else:
        user_id = user[0]

    cur.close()
    conn.close()

    session["user_id"] = user_id
    session["username"] = "guest"

    return redirect("/")


# -----------------------
# LOGIN
# -----------------------

@app.route("/login", methods=["POST"])
def login():
    """
    Authenticates a user by username.

    If the username exists, the user's information is stored in the session.
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
    Logs out the current user and clears session data.
    """

    session.clear()

    return redirect("/")


# -----------------------
# RUN APP
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)
