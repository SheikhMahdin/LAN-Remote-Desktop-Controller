# ============================================================
# server.py — Flask routes, SocketIO events, auth integration
# ============================================================

import threading
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit, disconnect

import control
import system
from screen import capture_screen, stream_screen
from auth import login_required, attempt_login, logout_user, is_authenticated, current_user
from config import SECRET_KEY, HOST, PORT, DEBUG

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

streaming_clients: set = set()


# ── HTTP Routes ──────────────────────────────────────────────

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=current_user())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if attempt_login(username, password, request.remote_addr):
            return redirect(url_for('index'))

        return render_template('login.html', error='Invalid username or password')

    return render_template('login.html', error=None)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# ── SocketIO Events ──────────────────────────────────────────

@socketio.on('connect')
def on_connect(auth=None):
    pass  # Session auth checked per-event, not on connect
    print(f"[server] Client connected: {request.sid}")
    emit('response', {'message': 'Authenticated connection established'})


@socketio.on('disconnect')
def on_disconnect():
    print(f"[server] Client disconnected: {request.sid}")
    streaming_clients.discard(request.sid)


@socketio.on('screenshot')
def on_screenshot():
    if not is_authenticated(): return
    try:
        emit('screenshot', capture_screen())
    except Exception as e:
        emit('response', {'message': f'Screenshot error: {e}'})


@socketio.on('start_stream')
def on_start_stream():
    if not is_authenticated(): return
    sid = request.sid
    if sid not in streaming_clients:
        streaming_clients.add(sid)
        threading.Thread(
            target=stream_screen,
            args=(socketio, sid, streaming_clients),
            daemon=True
        ).start()
        emit('response', {'message': 'Streaming started'})


@socketio.on('stop_stream')
def on_stop_stream():
    if not is_authenticated(): return
    streaming_clients.discard(request.sid)
    emit('response', {'message': 'Streaming stopped'})


@socketio.on('mouse_click')
def on_mouse_click(data):
    if not is_authenticated(): return
    try:
        msg = control.mouse_click(data['x'], data['y'], data.get('button', 'left'))
        emit('response', {'message': msg})
    except Exception as e:
        emit('response', {'message': f'Click error: {e}'})


@socketio.on('mouse_double_click')
def on_mouse_double_click(data):
    if not is_authenticated(): return
    try:
        msg = control.mouse_double_click(data['x'], data['y'])
        emit('response', {'message': msg})
    except Exception as e:
        emit('response', {'message': f'Double-click error: {e}'})


@socketio.on('type_text')
def on_type_text(data):
    if not is_authenticated(): return
    try:
        msg = control.type_text(data['text'])
        emit('response', {'message': msg})
    except Exception as e:
        emit('response', {'message': f'Typing error: {e}'})


@socketio.on('system_control')
def on_system_control(data):
    if not is_authenticated(): return
    try:
        msg = system.execute(data['action'], triggered_by=current_user())
        emit('response', {'message': msg})
    except Exception as e:
        emit('response', {'message': f'System control error: {e}'})


# ── Runner ───────────────────────────────────────────────────

def run():
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG, allow_unsafe_werkzeug=True)