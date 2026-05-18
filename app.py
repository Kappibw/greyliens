import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")


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
# GET ALL MESSAGES
# -------------------------
@app.route("/messages")
def messages():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT m.id, m.content, u.username, c.name
        FROM messages m
        JOIN users u ON m.author_id = u.id
        JOIN channels c ON m.channel_id = c.id
        ORDER BY m.id;
    """)

    rows = cur.fetchall()
    conn.close()

    return jsonify(rows)


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


if __name__ == "__main__":
    app.run(debug=True)