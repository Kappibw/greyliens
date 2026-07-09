import os
from flask import Flask, render_template, request, redirect, session

from db import get_conn
from auth import get_identity

app = Flask(__name__)

# Security configuration
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise ValueError("Environment variable 'SECRET_KEY' is not set")

print("SECRET_KEY is set")
print("APP FILE:", os.path.abspath(__file__))
print("TEMPLATE FOLDER:", app.template_folder)


@app.route("/")
def index():
    """
    Displays forum homepage with database content.
    """

    print("SESSION:", dict(session))
    print("IDENTITY:", get_identity())

    conn = get_conn()
    cur = conn.cursor()

    # Load channels
    cur.execute("""
        SELECT id, name
        FROM channels
        ORDER BY id;
    """)
    channels = cur.fetchall()

    # Load threads
    cur.execute("""
    SELECT
        t.id,
        t.title,
        t.content,
        u.username,
        t.created_at
    FROM threads t
    JOIN users u ON t.user_id = u.id
    ORDER BY t.id DESC;
""")
    threads = cur.fetchall() 
    # Load replies
    cur.execute("""
    SELECT
        r.id,
        r.content,
        u.username,
        r.created_at
    FROM replies r
    JOIN users u ON r.user_id = u.id
    ORDER BY r.id DESC;
""")
    replies = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "forum.html",
        channels=channels,
        threads=threads,
        replies=replies,
        user=session.get("username"),
        identity=get_identity()
    )


@app.route("/send", methods=["POST"])
def send():
    """
    Creates a new message.
    """

    if "user_id" not in session:
        return "Not allowed (logged out)", 403

    content = request.form.get("content")

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
        cur.close()
        conn.close()
        return "Channel not found", 500

    channel_id = channel[0]

    cur.execute("""
        INSERT INTO messages (channel_id, author_id, content)
        VALUES (%s, %s, %s)
    """, (channel_id, user_id, content))

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/")


@app.route("/guest-login")
def guest_login():

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


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)