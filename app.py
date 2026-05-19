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
    return jsonify({"message": "Flask is running 🚀"})


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
        SELECT id, content, author_id, channel_id, created_at
        FROM messages
        ORDER BY id;
    """)

    rows = cur.fetchall()
    conn.close()

    messages = []
    for r in rows:
        messages.append({
            "id": r[0],
            "content": r[1],
            "author_id": r[2],
            "channel_id": r[3],
            "created_at": r[4].isoformat() if r[4] else None
        })

    return jsonify(messages)


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