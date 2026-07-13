
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
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise ValueError("Environment variable 'SECRET_KEY' is not set")

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
    if "user_id" not in session:
        return "Not allowed (logged out)", 403

    content = request.form.get("content", "").strip()

    if not content:
        return "Message cannot be empty", 400

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
# LOGIN
# -----------------------
@app.route("/login", methods=["POST"])
def login():

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
    session.clear()
    return redirect("/")


# -----------------------
# RUN
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)

