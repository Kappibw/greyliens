from flask import session

def get_identity():
    if "user_id" not in session:
        return "logged_out"

    if session.get("username") == "guest":
        return "guest"

    return "db_user"