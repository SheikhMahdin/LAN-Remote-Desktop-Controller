# ============================================================
# system.py — OS-level power management
# ============================================================

import os
import platform

_SYSTEM = platform.system()

_COMMANDS = {
    'Windows': {
        'shutdown': ('shutdown /s /t 5',                              'PC will shutdown in 5 seconds...'),
        'restart':  ('shutdown /r /t 5',                              'PC will restart in 5 seconds...'),
        'sleep':    ('rundll32.exe powrprof.dll,SetSuspendState 0,1,0','PC is going to sleep...'),
    },
    'Linux': {
        'shutdown': ('shutdown -h +1',    'PC will shutdown in 1 minute...'),
        'restart':  ('shutdown -r +1',    'PC will restart in 1 minute...'),
        'sleep':    ('systemctl suspend', 'PC is going to sleep...'),
    },
    'Darwin': {
        'shutdown': ('sudo shutdown -h +1', 'PC will shutdown in 1 minute...'),
        'restart':  ('sudo shutdown -r +1', 'PC will restart in 1 minute...'),
        'sleep':    ('pmset sleepnow',      'PC is going to sleep...'),
    },
}


def execute(action: str, triggered_by: str = 'unknown') -> str:
    """Execute a power action and return a status message."""
    if _SYSTEM not in _COMMANDS:
        return f'Unsupported operating system: {_SYSTEM}'
    if action not in _COMMANDS[_SYSTEM]:
        return f'Unknown action: {action}'

    cmd, message = _COMMANDS[_SYSTEM][action]
    print(f"[system] ⚠️ '{action}' triggered by '{triggered_by}'")
    os.system(cmd)
    return message