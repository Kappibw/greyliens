import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT m.id, m.content, u.username, c.name, m.created_at
        FROM messages m
        JOIN users u ON m.author_id = u.id
        JOIN channels c ON m.channel_id = c.id
        ORDER BY m.id DESC;
    """)

    messages = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("forum.html", messages=messages)


@app.route("/send", methods=["POST"])
def send():
    content = request.form.get("content")

    conn = get_conn()
    cur = conn.cursor()

    # always use default MVP values for now
    cur.execute("SELECT id FROM users WHERE username='guest' LIMIT 1;")
    user_id = cur.fetchone()[0]

    cur.execute("SELECT id FROM channels WHERE name='general' LIMIT 1;")
    channel_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO messages (channel_id, author_id, content)
        VALUES (%s, %s, %s)
    """, (channel_id, user_id, content))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)