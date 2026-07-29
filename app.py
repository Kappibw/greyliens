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

    Retrieves forum data from the database including channels,
    threads, and messages with their associated users. The retrieved
    data is passed to the forum template to render the sidebar,
    thread list, and conversation view.
    """

    conn = get_conn()
    cur = conn.cursor()

    # -----------------------
    # Load Channels
    # -----------------------

    try:
        cur.execute("""
            SELECT id, name
            FROM channels
            ORDER BY id;
        """)

        channels = cur.fetchall()

    except Exception:
        conn.rollback()
        channels = []


    # -----------------------
    # Load Threads
    # -----------------------

    try:
        cur.execute("""
            SELECT
                t.id,
                t.title,
                u.username,
                t.created_at
            FROM threads t
            LEFT JOIN users u
                ON t.author_id = u.id
            ORDER BY t.created_at DESC;
        """)

        threads = cur.fetchall()

    except Exception:
        conn.rollback()
        threads = []


    # -----------------------
    # Load Messages
    # -----------------------

    try:
        cur.execute("""
            SELECT
                m.id,
                m.thread_id,
                m.content,
                u.username,
                m.created_at
            FROM messages m
            LEFT JOIN users u
                ON m.user_id = u.id
            ORDER BY m.created_at ASC;
        """)

        messages = cur.fetchall()

    except Exception:
        conn.rollback()
        messages = []


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
# SEND MESSAGE
# -----------------------
@app.route("/send", methods=["POST"])
def send():
    """
    Creates a new message from the logged-in user and posts it to the
    hard-coded "general" channel. The user cannot choose which channel
    to post to through this endpoint.
    """

    if "user_id" not in session:
        return "Not allowed (logged out)", 403


    content = request.form.get("content", "").strip()


    if not content:
        return "Empty message not allowed", 400


    conn = get_conn()
    cur = conn.cursor()


    try:

        # Find general channel
        cur.execute("""
            SELECT id
            FROM channels
            WHERE name = 'general'
            LIMIT 1;
        """)

        channel = cur.fetchone()


        if not channel:
            return "General channel does not exist", 404


        channel_id = channel[0]


        # Insert message
        cur.execute("""
            INSERT INTO messages
            (
                channel_id,
                user_id,
                content
            )
            VALUES (%s, %s, %s);
        """,
        (
            channel_id,
            session["user_id"],
            content
        ))


        conn.commit()


    except Exception as e:

        conn.rollback()

        print("SEND ERROR:", e)

        return "Failed to send message", 500


    finally:

        cur.close()
        conn.close()


    return redirect("/")

# -----------------------
# VIEW THREAD
# -----------------------

@app.route("/thread/<int:thread_id>")
def view_thread(thread_id):
    """
    Displays a single thread and its replies.
    """

    conn = get_conn()
    cur = conn.cursor()

    try:

        # Get thread details
        cur.execute("""
            SELECT
                t.id,
                t.title,
                u.username,
                t.created_at
            FROM threads t
            LEFT JOIN users u
                ON t.author_id = u.id
            WHERE t.id = %s;
        """, (thread_id,))

        thread = cur.fetchone()


        # Get replies
        cur.execute("""
            SELECT
                r.content,
                r.created_at,
                u.username
            FROM replies r
            LEFT JOIN users u
                ON r.user_id = u.id
            WHERE r.thread_id = %s
            ORDER BY r.created_at ASC;
        """, (thread_id,))

        replies = cur.fetchall()


    except Exception as e:

        print("THREAD ERROR:", e)

        thread = None
        replies = []


    finally:

        cur.close()
        conn.close()


    return render_template(
        "thread.html",
        thread=thread,
        replies=replies,
        user_id=session.get("user_id")
    )
# -----------------------
# CREATE REPLY
# -----------------------

@app.route("/replies", methods=["POST"])
def create_reply():

    if "user_id" not in session:
        return "Not allowed", 403


    thread_id = request.form.get("thread_id")
    content = request.form.get("content", "").strip()


    if not content:
        return "Reply cannot be empty", 400


    conn = get_conn()
    cur = conn.cursor()


    try:

        cur.execute("""
            INSERT INTO replies
            (
                thread_id,
                user_id,
                content
            )
            VALUES (%s, %s, %s);
        """,
        (
            thread_id,
            session["user_id"],
            content
        ))


        conn.commit()


    except Exception as e:

        conn.rollback()

        print("REPLY ERROR:", e)

        return "Failed to create reply", 500


    finally:

        cur.close()
        conn.close()


    return redirect(f"/thread/{thread_id}")

# -----------------------
# LOGIN
# -----------------------

@app.route("/login", methods=["POST"])
def login():
    """
    Logs in an existing user by username and stores the user's
    identity in the session.
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
    """,
    (username,))


    user = cur.fetchone()


    cur.close()
    conn.close()


    if not user:
        return "User not found", 404


    session["user_id"] = user[0]
    session["username"] = user[1]


    return redirect("/")



# -----------------------
# GUEST LOGIN
# -----------------------

@app.route("/guest-login")
def guest_login():

    conn = get_conn()
    cur = conn.cursor()


    try:

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
                VALUES ('guest')
                RETURNING id;
            """)

            user = cur.fetchone()

            conn.commit()


        session["user_id"] = user[0]
        session["username"] = "guest"


    except Exception:

        conn.rollback()
        return "Guest login failed", 500


    finally:

        cur.close()
        conn.close()


    return redirect("/")



# -----------------------
# LOGOUT
# -----------------------

@app.route("/logout")
def logout():
    """Clears the current user's session"""
    session.clear()

    return redirect("/")



# -----------------------
# RUN APP
# -----------------------

if __name__ == "__main__":
    app.run(debug=True)