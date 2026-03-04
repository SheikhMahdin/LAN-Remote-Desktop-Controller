# ============================================================
# auth.py — Authentication: login, logout, session guard
# ============================================================

from functools import wraps
from flask import session, redirect, url_for, request
from werkzeug.security import check_password_hash
from config import USERNAME, PASSWORD_HASH


def login_required(f):
    """Decorator — redirect to login if not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def attempt_login(username: str, password: str, remote_addr: str) -> bool:
    """Validate credentials and log the attempt. Returns True on success."""
    if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
        session['logged_in'] = True
        session['username'] = username
        print(f"[auth] ✅ '{username}' logged in from {remote_addr}")
        return True

    print(f"[auth] ❌ Failed login attempt from {remote_addr}")
    return False


def logout_user():
    """Clear the session and log the event."""
    username = session.get('username', 'Unknown')
    session.clear()
    print(f"[auth] 👋 '{username}' logged out")


def is_authenticated() -> bool:
    """Check if the current session is authenticated."""
    return bool(session.get('logged_in'))


def current_user() -> str:
    """Return the logged-in username."""
    return session.get('username', '')