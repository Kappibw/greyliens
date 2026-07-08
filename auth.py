from flask import session

"""
Identity helper module.

Determines the current authentication state
based on Flask session data.
"""

def get_identity():
    """
    Returns the current user's identity state.

    Returns:
        - "logged_out" → no active session
        - "guest" → guest login session
        - "db_user" → registered database user
    """

    if "user_id" not in session:
        return "logged_out"

    if session.get("username") == "guest":
        return "guest"

    return "db_user"


