
import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

# Railway PostgreSQL connection string (environment variable)
DATABASE_URL = os.getenv("DATABASE_URL")


# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_connection():
    return psycopg2.connect(DATABASE_URL)


# -------------------------
# HOME ROUTE
# -------------------------
@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()

    # Example table: messages (adjust if your table name differs)
    cur.execute("""
        SELECT username, message
        FROM messages
        ORDER BY id ASC;
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("forum.html", messages=data)


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)

