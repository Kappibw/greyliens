from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
import os

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
# HOME MESSAGES
# -----------------------

@app.route("/")
def index():
    """
    Displays the forum homepage.
    Retrieves messages with their authors and channels then render the forum page.
    """

    print("SESSION:", dict(session))
    print("IDENTITY:", get_identity())

    conn = get_conn()
    cur = conn.cursor()

    # Channels
    cur.execute("""
        SELECT id, name
        FROM channels
        ORDER BY id;
    """)
    channels = cur.fetchall()

    # Messages
    cur.execute("""
        SELECT 
            m.id,
            m.content,
            u.username,
            c.name,
            m.created_at
        FROM messages m
        JOIN users u ON m.user_id = u.id
        JOIN channels c ON m.channel_id = c.id
        ORDER BY m.id DESC;
    """)
    messages = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "forum.html",
        channels=channels,
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
    Creates a new message in the general channel.
    Only logged-in users can send messages.
    """

    if "user_id" not in session:
        return "Not allowed (logged out)", 403

    content = request.form.get("content", "").strip()

    if not content:
        return "Empty message not allowed", 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM channels
        LIMIT 1;
    """)

    channel = cur.fetchone()

    if not channel:
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
    Logs a user into the application using the guest account.
    """

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username = 'guest' LIMIT 1;"
    )

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
    Authenticates a user by username.
    If the username exists, the user's information is stored in session
    """
    username = request.form.get("username", "").strip()

    if not username:
        return "Username required", 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username
        FROM users
        WHERE username=%s;
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

