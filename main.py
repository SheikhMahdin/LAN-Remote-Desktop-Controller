# ============================================================
# main.py — Entry point
# ============================================================

import socket
from config import PORT, USERNAME
from server import run


def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


if __name__ == '__main__':
    local_ip = get_local_ip()

    print('=' * 55)
    print('   🔐 LAN Remote Desktop Controller — Secure')
    print('=' * 55)
    print(f'\n  Username: {USERNAME}')
    print(f'  Password: admin123  ← CHANGE THIS in config.py')
    print(f'\n  Local:    http://localhost:{PORT}')
    print(f'  Network:  http://{local_ip}:{PORT}')
    print('\n  Press Ctrl+C to stop.\n')
    print('=' * 55)

    run()