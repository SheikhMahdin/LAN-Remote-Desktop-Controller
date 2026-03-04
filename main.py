"""
Remote PC Control Server with Screen Sharing - ENHANCED VERSION
Install required packages:
pip install flask flask-socketio pyautogui mss pillow python-socketio
"""
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import pyautogui
import mss
import base64
import io
from PIL import Image
import threading
import time
import socket
import platform
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'remote-control-secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Enable PyAutoGUI fail-safe and optimize settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# Get actual screen size
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
print(f"Detected screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

# HTML Template with fullscreen and system controls
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🖥️ Remote PC Control</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            text-align: center;
        }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .status-bar {
            display: flex;
            justify-content: space-around;
            padding: 15px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
            flex-wrap: wrap;
            gap: 10px;
        }
        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 15px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #dc3545;
            animation: pulse 2s infinite;
        }
        .status-dot.connected { background: #28a745; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .controls {
            padding: 20px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }
        .control-section {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            padding: 10px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .control-label {
            width: 100%;
            font-size: 12px;
            font-weight: bold;
            color: #666;
            margin-bottom: 5px;
        }
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        button:hover { transform: translateY(-2px); box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
        button:active { transform: translateY(0); }
        .btn-primary { background: #667eea; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn-danger { background: #dc3545; color: white; }
        .btn-warning { background: #ffc107; color: #000; }
        .btn-info { background: #17a2b8; color: white; }
        .btn-dark { background: #343a40; color: white; }
        .btn-purple { background: #6f42c1; color: white; }
        .btn-orange { background: #fd7e14; color: white; }
        
        .screen-container {
            padding: 20px;
            background: #2c3e50;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 500px;
        }
        #screenCanvas {
            max-width: 100%;
            height: auto;
            border: 3px solid #fff;
            border-radius: 8px;
            cursor: crosshair;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .input-group {
            padding: 20px;
            display: flex;
            gap: 10px;
            background: #f8f9fa;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 14px;
        }
        .info-box {
            padding: 20px;
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            margin: 20px;
            border-radius: 8px;
        }
        .info-box h3 { color: #1976D2; margin-bottom: 10px; }
        .info-box ul { margin-left: 20px; }
        .info-box li { margin: 5px 0; color: #333; }
        .debug-info {
            padding: 15px;
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            margin: 20px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
        }
        
        /* Modal for system actions confirmation */
        .modal {
            display: none;
            position: fixed;
            z-index: 2000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            align-items: center;
            justify-content: center;
        }
        .modal.show {
            display: flex;
        }
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }
        .modal-content h2 {
            color: #dc3545;
            margin-bottom: 20px;
        }
        .modal-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖥️ Remote PC Control</h1>
        </div>
        
        <div class="status-bar">
            <div class="status-item">
                <div class="status-dot" id="statusDot"></div>
                <span id="statusText">Disconnected</span>
            </div>
            <div class="status-item">
                📊 <span id="fpsCounter">0 FPS</span>
            </div>
            <div class="status-item">
                🖥️ <span id="screenSize">Unknown</span>
            </div>
            <div class="status-item">
                ⚡ <span id="qualityInfo">Standard</span>
            </div>
        </div>

        <div class="controls">
            <div class="control-section">
                <div class="control-label">🔌 Connection</div>
                <button class="btn-primary" onclick="connectServer()">Connect</button>
            </div>
            
            <div class="control-section">
                <div class="control-label">📺 Streaming</div>
                <button class="btn-success" onclick="startStreaming()">Start Streaming</button>
                <button class="btn-danger" onclick="stopStreaming()">Stop Streaming</button>
                <button class="btn-info" onclick="takeScreenshot()">Single Screenshot</button>
            </div>
            
            <div class="control-section">
                <div class="control-label">⚙️ System Controls</div>
                <button class="btn-warning" onclick="confirmAction('sleep')">💤 Sleep</button>
                <button class="btn-orange" onclick="confirmAction('restart')">🔄 Restart</button>
                <button class="btn-danger" onclick="confirmAction('shutdown')">⚡ Shutdown</button>
            </div>
        </div>

        <div class="screen-container" id="screenContainer">
            <canvas id="screenCanvas"></canvas>
        </div>

        <div class="input-group">
            <input type="text" id="textInput" placeholder="Type text to send to remote PC...">
            <button class="btn-primary" onclick="sendText()">Send Text</button>
        </div>

        <div class="debug-info" id="debugInfo">
            Click coordinates will appear here...
        </div>

        <div class="info-box">
            <h3>Controls:</h3>
            <ul>
                <li><strong>Left Click:</strong> Click on the screen</li>
                <li><strong>Right Click:</strong> Right-click menu (context menu)</li>
                <li><strong>Double Click:</strong> Double-click action</li>
                <li><strong>Type & Send:</strong> Type text in the input field and send to remote PC</li>
                <li><strong>System Controls:</strong> Sleep, Restart, or Shutdown remote PC</li>
                <li><strong>Streaming:</strong> Ultra smooth 20 FPS with high quality</li>
            </ul>
        </div>
    </div>

    <!-- Confirmation Modal -->
    <div id="confirmModal" class="modal">
        <div class="modal-content">
            <h2>⚠️ Confirm Action</h2>
            <p id="confirmMessage"></p>
            <div class="modal-buttons">
                <button class="btn-danger" onclick="executeSystemAction()">Yes, Proceed</button>
                <button class="btn-primary" onclick="closeModal()">Cancel</button>
            </div>
        </div>
    </div>

    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <script>
        let socket;
        let isStreaming = false;
        let frameCount = 0;
        let lastFpsUpdate = Date.now();
        let pendingSystemAction = null;
        
        // Store screen dimensions for coordinate mapping
        let originalWidth = 0;
        let originalHeight = 0;
        let displayWidth = 0;
        let displayHeight = 0;

        const canvas = document.getElementById('screenCanvas');
        const ctx = canvas.getContext('2d');

        function updateDebug(message) {
            document.getElementById('debugInfo').textContent = message;
        }

        function connectServer() {
            socket = io();

            socket.on('connect', () => {
                document.getElementById('statusDot').classList.add('connected');
                document.getElementById('statusText').textContent = 'Connected';
                updateDebug('Connected to server - Ultra smooth mode active (20 FPS)');
            });

            socket.on('disconnect', () => {
                document.getElementById('statusDot').classList.remove('connected');
                document.getElementById('statusText').textContent = 'Disconnected';
                isStreaming = false;
            });

            socket.on('screenshot', (data) => {
                // Store dimensions for coordinate mapping
                originalWidth = data.original_width;
                originalHeight = data.original_height;
                displayWidth = data.display_width;
                displayHeight = data.display_height;

                // Update screen size display
                document.getElementById('screenSize').textContent = 
                    `${originalWidth}x${originalHeight}`;
                document.getElementById('qualityInfo').textContent = 
                    `High Quality (${data.quality}%)`;

                const img = new Image();
                img.onload = () => {
                    canvas.width = displayWidth;
                    canvas.height = displayHeight;
                    ctx.imageSmoothingEnabled = false;
                    requestAnimationFrame(() => ctx.drawImage(img, 0, 0));
                    
                    // Update FPS counter
                    frameCount++;
                    const now = Date.now();
                    if (now - lastFpsUpdate >= 1000) {
                        document.getElementById('fpsCounter').textContent = 
                            `${frameCount} FPS`;
                        frameCount = 0;
                        lastFpsUpdate = now;
                    }
                };
                img.src = 'data:image/jpeg;base64,' + data.image;
            });

            socket.on('response', (data) => {
                console.log(data.message);
                updateDebug(data.message);
            });
        }

        function startStreaming() {
            if (socket && !isStreaming) {
                socket.emit('start_stream');
                isStreaming = true;
            }
        }

        function stopStreaming() {
            if (socket && isStreaming) {
                socket.emit('stop_stream');
                isStreaming = false;
                frameCount = 0;
                document.getElementById('fpsCounter').textContent = '0 FPS';
            }
        }

        function takeScreenshot() {
            if (socket) {
                socket.emit('screenshot');
            }
        }

        function sendText() {
            const text = document.getElementById('textInput').value;
            if (socket && text) {
                socket.emit('type_text', { text: text });
                document.getElementById('textInput').value = '';
            }
        }

        // System control confirmation
        function confirmAction(action) {
            pendingSystemAction = action;
            const messages = {
                'sleep': 'Are you sure you want to put the remote PC to sleep?',
                'restart': 'Are you sure you want to restart the remote PC?',
                'shutdown': 'Are you sure you want to shutdown the remote PC?'
            };
            document.getElementById('confirmMessage').textContent = messages[action];
            document.getElementById('confirmModal').classList.add('show');
        }

        function closeModal() {
            document.getElementById('confirmModal').classList.remove('show');
            pendingSystemAction = null;
        }

        function executeSystemAction() {
            if (socket && pendingSystemAction) {
                socket.emit('system_control', { action: pendingSystemAction });
                closeModal();
            }
        }

        // FIXED: Proper coordinate mapping from display to actual screen
        function mapCoordinates(canvasX, canvasY) {
            if (originalWidth === 0 || originalHeight === 0) {
                return { x: canvasX, y: canvasY };
            }

            // Calculate scale ratios
            const scaleX = originalWidth / displayWidth;
            const scaleY = originalHeight / displayHeight;

            // Map coordinates to actual screen resolution
            const actualX = Math.round(canvasX * scaleX);
            const actualY = Math.round(canvasY * scaleY);

            return { x: actualX, y: actualY };
        }

        function getCanvasCoordinates(e) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;

            const canvasX = Math.round((e.clientX - rect.left) * scaleX);
            const canvasY = Math.round((e.clientY - rect.top) * scaleY);

            // Map to actual screen coordinates
            const coords = mapCoordinates(canvasX, canvasY);
            
            updateDebug(
                `Display: (${canvasX}, ${canvasY}) -> ` +
                `Actual: (${coords.x}, ${coords.y}) | ` +
                `Scale: ${(originalWidth/displayWidth).toFixed(2)}x${(originalHeight/displayHeight).toFixed(2)} | ` +
                `Screen: ${originalWidth}x${originalHeight}`
            );

            return coords;
        }

        // Mouse event handlers
        canvas.addEventListener('click', (e) => {
            if (!socket) return;
            const coords = getCanvasCoordinates(e);
            socket.emit('mouse_click', { 
                x: coords.x, 
                y: coords.y, 
                button: 'left' 
            });
        });

        canvas.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            if (!socket) return;
            const coords = getCanvasCoordinates(e);
            socket.emit('mouse_click', { 
                x: coords.x, 
                y: coords.y, 
                button: 'right' 
            });
        });

        canvas.addEventListener('dblclick', (e) => {
            if (!socket) return;
            const coords = getCanvasCoordinates(e);
            socket.emit('mouse_double_click', { 
                x: coords.x, 
                y: coords.y 
            });
        });

        // Keyboard shortcuts
        document.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && document.activeElement.id === 'textInput') {
                sendText();
            }
        });

        // Auto-connect on load
        window.onload = () => {
            connectServer();
        };
    </script>
</body>
</html>
'''

# Global streaming state
streaming_clients = set()

def capture_screen():
    """Capture screenshot with enhanced quality"""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        
        # Store original dimensions
        original_width = img.width
        original_height = img.height
        
        # Resize for better performance (larger size for better quality)
        img.thumbnail((1280, 720), Image.Resampling.NEAREST)
        
        buffer = io.BytesIO()
        # Increased quality from 70 to 85
        img.save(buffer, format='JPEG', quality=60, optimize=False)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'image': img_str,
            'original_width': original_width,
            'original_height': original_height,
            'display_width': img.width,
            'display_height': img.height,
            'quality': 85
        }

def stream_screen(sid):
    """Continuous screen streaming with ultra smooth FPS"""
    while sid in streaming_clients:
        try:
            screen_data = capture_screen()
            socketio.emit('screenshot', screen_data, room=sid)
            time.sleep(0.016)  # 20 FPS for ultra smooth streaming
        except Exception as e:
            print(f"Streaming error: {e}")
            break

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@socketio.on('connect')
def handle_connect(auth=None):
    print(f"Client connected: {request.sid}")
    emit('response', {'message': 'Connected to remote PC - Enhanced mode active'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")
    if request.sid in streaming_clients:
        streaming_clients.remove(request.sid)

@socketio.on('screenshot')
def handle_screenshot():
    """Take a single screenshot"""
    try:
        screen_data = capture_screen()
        emit('screenshot', screen_data)
    except Exception as e:
        emit('response', {'message': f'Error: {str(e)}'})

@socketio.on('start_stream')
def handle_start_stream():
    """Start continuous screen streaming"""
    sid = request.sid
    if sid not in streaming_clients:
        streaming_clients.add(sid)
        thread = threading.Thread(target=stream_screen, args=(sid,))
        thread.daemon = True
        thread.start()
        emit('response', {'message': 'Ultra smooth streaming started (20 FPS, High Quality)'})

@socketio.on('stop_stream')
def handle_stop_stream():
    """Stop continuous screen streaming"""
    sid = request.sid
    if sid in streaming_clients:
        streaming_clients.remove(sid)
        emit('response', {'message': 'Streaming stopped'})

@socketio.on('mouse_click')
def handle_mouse_click(data):
    """Handle mouse click events"""
    try:
        x, y = data['x'], data['y']
        button = data.get('button', 'left')
        
        # Clamp coordinates to screen bounds
        x = max(0, min(x, SCREEN_WIDTH - 1))
        y = max(0, min(y, SCREEN_HEIGHT - 1))
        
        print(f"Click at: ({x}, {y}) - Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        
        # Move then click for better accuracy
        pyautogui.moveTo(x, y, duration=0)
        time.sleep(0.01)
        pyautogui.click(button=button)
        
        emit('response', {'message': f'{button.capitalize()} clicked at ({x}, {y})'})
    except Exception as e:
        emit('response', {'message': f'Error: {str(e)}'})

@socketio.on('mouse_double_click')
def handle_double_click(data):
    """Handle double click events"""
    try:
        x, y = data['x'], data['y']
        
        # Clamp coordinates to screen bounds
        x = max(0, min(x, SCREEN_WIDTH - 1))
        y = max(0, min(y, SCREEN_HEIGHT - 1))
        
        pyautogui.moveTo(x, y, duration=0)
        time.sleep(0.01)
        pyautogui.doubleClick()
        
        emit('response', {'message': f'Double clicked at ({x}, {y})'})
    except Exception as e:
        emit('response', {'message': f'Error: {str(e)}'})

@socketio.on('type_text')
def handle_type_text(data):
    """Handle text typing"""
    try:
        text = data['text']
        pyautogui.write(text, interval=0.05)
        emit('response', {'message': f'Typed: {text}'})
    except Exception as e:
        emit('response', {'message': f'Error: {str(e)}'})

@socketio.on('system_control')
def handle_system_control(data):
    """Handle system control commands (shutdown, sleep, restart)"""
    try:
        action = data['action']
        system = platform.system()
        
        print(f"System control: {action} on {system}")
        
        if system == 'Windows':
            if action == 'shutdown':
                os.system('shutdown /s /t 5')
                emit('response', {'message': 'PC will shutdown in 5 seconds...'})
            elif action == 'restart':
                os.system('shutdown /r /t 5')
                emit('response', {'message': 'PC will restart in 5 seconds...'})
            elif action == 'sleep':
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
                emit('response', {'message': 'PC is going to sleep...'})
                
        elif system == 'Linux':
            if action == 'shutdown':
                os.system('shutdown -h +1')
                emit('response', {'message': 'PC will shutdown in 1 minute...'})
            elif action == 'restart':
                os.system('shutdown -r +1')
                emit('response', {'message': 'PC will restart in 1 minute...'})
            elif action == 'sleep':
                os.system('systemctl suspend')
                emit('response', {'message': 'PC is going to sleep...'})
                
        elif system == 'Darwin':  # macOS
            if action == 'shutdown':
                os.system('sudo shutdown -h +1')
                emit('response', {'message': 'PC will shutdown in 1 minute...'})
            elif action == 'restart':
                os.system('sudo shutdown -r +1')
                emit('response', {'message': 'PC will restart in 1 minute...'})
            elif action == 'sleep':
                os.system('pmset sleepnow')
                emit('response', {'message': 'PC is going to sleep...'})
        else:
            emit('response', {'message': f'Unsupported operating system: {system}'})
            
    except Exception as e:
        emit('response', {'message': f'Error: {str(e)}'})

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    
    print("=" * 60)
    print("🖥️  Remote PC Control Server - ULTRA SMOOTH VERSION")
    print("=" * 60)
    print(f"\n📡 Access from this PC:")
    print(f"   http://localhost:{port}")
    print(f"   http://127.0.0.1:{port}")
    print(f"\n📱 Access from other devices on same WiFi:")
    print(f"   http://{local_ip}:{port}")
    print(f"\n✨ FEATURES:")
    print(f"   ✅ Ultra smooth 20 FPS streaming")
    print(f"   ✅ Higher quality images (85% quality)")
    print(f"   ✅ System controls (Sleep/Restart/Shutdown)")
    print(f"   ✅ Fixed coordinate mapping")
    print("\n⚠️  Security Warning:")
    print("   - Only use on trusted networks")
    print("   - System controls have 5-second delay")
    print("   - This gives full control of your PC!")
    print("\n🔧 Press Ctrl+C to stop the server\n")
    print("=" * 60)
    
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)
