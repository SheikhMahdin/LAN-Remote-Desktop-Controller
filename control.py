# ============================================================
# control.py — Mouse and keyboard control via PyAutoGUI
# ============================================================

import pyautogui
import time
from config import MOUSE_MOVE_DURATION, MOUSE_CLICK_DELAY, TYPING_INTERVAL, FAILSAFE, PAUSE

pyautogui.FAILSAFE = FAILSAFE
pyautogui.PAUSE = PAUSE

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


def _clamp(x: int, y: int) -> tuple:
    x = max(0, min(x, SCREEN_WIDTH - 1))
    y = max(0, min(y, SCREEN_HEIGHT - 1))
    return x, y


def mouse_click(x: int, y: int, button: str = 'left') -> str:
    x, y = _clamp(x, y)
    pyautogui.moveTo(x, y, duration=MOUSE_MOVE_DURATION)
    time.sleep(MOUSE_CLICK_DELAY)
    pyautogui.click(button=button)
    return f'{button.capitalize()} clicked at ({x}, {y})'


def mouse_double_click(x: int, y: int) -> str:
    x, y = _clamp(x, y)
    pyautogui.moveTo(x, y, duration=MOUSE_MOVE_DURATION)
    time.sleep(MOUSE_CLICK_DELAY)
    pyautogui.doubleClick()
    return f'Double clicked at ({x}, {y})'


def type_text(text: str) -> str:
    pyautogui.write(text, interval=TYPING_INTERVAL)
    return f'Typed: {text}'