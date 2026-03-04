# ============================================================
# screen.py — Screen capture and streaming
# ============================================================

import mss
import base64
import io
from PIL import Image
import time
from config import CAPTURE_WIDTH, CAPTURE_HEIGHT, JPEG_QUALITY, STREAM_INTERVAL


def capture_screen() -> dict:
    """Capture the primary monitor and return compressed JPEG data."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

        original_width = img.width
        original_height = img.height

        img.thumbnail((CAPTURE_WIDTH, CAPTURE_HEIGHT), Image.Resampling.NEAREST)

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=JPEG_QUALITY, optimize=False)
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return {
            'image': img_str,
            'original_width': original_width,
            'original_height': original_height,
            'display_width': img.width,
            'display_height': img.height,
            'quality': JPEG_QUALITY,
        }


def stream_screen(socketio, sid: str, streaming_clients: set):
    """Continuously stream screen frames to a connected client."""
    while sid in streaming_clients:
        try:
            screen_data = capture_screen()
            socketio.emit('screenshot', screen_data, room=sid)
            time.sleep(STREAM_INTERVAL)
        except Exception as e:
            print(f"[screen] Streaming error for {sid}: {e}")
            break