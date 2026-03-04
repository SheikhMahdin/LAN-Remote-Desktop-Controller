# ============================================================
# config.py — All app settings and constants
# ============================================================

from werkzeug.security import generate_password_hash

# Server
PORT = 5000
SECRET_KEY = 'a1b2c3d4e5f6-change-this-to-any-long-random-string'
HOST = '0.0.0.0'
DEBUG = False


# Credentials — change before use!
USERNAME = "admin"
PASSWORD_HASH = generate_password_hash("admin123")

# Streaming
FPS = 60
STREAM_INTERVAL = 1 / FPS

# Screen capture
CAPTURE_WIDTH = 1280
CAPTURE_HEIGHT = 720
JPEG_QUALITY = 60

# PyAutoGUI
FAILSAFE = True
PAUSE = 0
MOUSE_MOVE_DURATION = 0
MOUSE_CLICK_DELAY = 0.01
TYPING_INTERVAL = 0.05