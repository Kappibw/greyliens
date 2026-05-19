import os
import psycopg2
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Load database URL from environment variables (Railway / .env)
DATABASE_URL = os.getenv("DATABASE_URL")


# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_conn():
    return psycopg2.connect(DATABASE_URL)


# -------------------------
# HOME ROUTE
# -------------------------
@app.route("/")
def home():
    return "Hello, Flask!"


# -------------------------
# TEST DATABASE CONNECTION
# -------------------------
@app.route("/test-db")
def test_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT NOW();")
    result = cur.fetchone()

    conn.close()

    return jsonify({"db_time": result[0]})


# -------------------------
# GET ALL MESSAGES (JSON API)
# -------------------------
@app.route("/messages")
def messages():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT m.id, m.content, m.author_id, m.channel_id, c.name
        FROM messages m
        JOIN channels c ON m.channel_id = c.id
        ORDER BY m.id;
    """)

    rows = cur.fetchall()
    conn.close()

    return jsonify(rows)


# -------------------------
# FORUM PAGE (HTML UI)
# -------------------------
@app.route("/forum")
def forum():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, content, author_id, channel_id, created_at
        FROM messages
        ORDER BY created_at DESC;
    """)

    messages = cur.fetchall()
    conn.close()

    return render_template("forum.html", messages=messages)


# -------------------------
# UPDATE SAMPLE MESSAGE
# -------------------------
@app.route("/edit-sample-message")
def edit_sample_message():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE messages
        SET content = 'Hello everyone 👋 (edited message)',
            edited = TRUE,
            updated_at = NOW()
        WHERE id = 1;
    """)

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Sample message updated successfully",
        "updated_message_id": 1
    })


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)