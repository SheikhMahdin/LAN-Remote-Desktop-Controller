# LAN-Remote-Desktop-Controller
# 🖥️ LAN Remote Desktop Controller

> Browser-based remote desktop tool for your local network — live screen streaming, full mouse & keyboard control, and system power management, protected by password authentication.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 Password Login | Secure session-based authentication |
| 📺 Live Streaming | Up to 60 FPS screen streaming |
| 🖱️ Mouse Control | Left click, right click, double click |
| ⌨️ Keyboard Input | Send text to the remote PC |
| ⚡ Power Controls | Sleep, Restart, Shutdown (with confirmation) |
| 🌐 Cross-Device | Works from any browser — PC, phone, tablet |
| 🔁 Auto-Start | Runs silently on Windows boot |

---

## 📁 Project Structure

```
web_control/
├── main.py              # Entry point — run this to start
├── server.py            # Flask routes & SocketIO events
├── auth.py              # Login, logout, session management
├── screen.py            # Screen capture & streaming logic
├── control.py           # Mouse & keyboard control
├── system.py            # Shutdown / restart / sleep
├── config.py            # All settings in one place
├── templates/
│   ├── login.html       # Login page
│   └── index.html       # Main control UI
├── static/
│   └── app.js           # Frontend JavaScript
├── requirements.txt     # Python dependencies
└── start_remote.bat     # Windows auto-start script
```

---

## 📋 Requirements

- **OS:** Windows 10 / 11 (also works on Linux and macOS)
- **Python:** 3.10 or higher
- **Network:** Both devices must be on the same Wi-Fi

---

## 🚀 Setup & Installation

### Step 1 — Install Dependencies

Open Command Prompt and run:

```cmd
pip install flask flask-socketio pyautogui mss pillow python-socketio werkzeug
```

Or use the requirements file:

```cmd
pip install -r requirements.txt
```

---

### Step 2 — Change the Default Password

Open `config.py` and update the credentials:

```python
USERNAME = "admin"           # Change this
PASSWORD_HASH = generate_password_hash("admin123")  # Change this
```

To generate a secure password hash, run this in Python:

```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("your_new_password"))
```

Then paste the output as the value of `PASSWORD_HASH`.

Also update the secret key:

```python
SECRET_KEY = 'a1b2c3d4e5f6-change-this-to-any-long-random-string'
```

---

### Step 3 — Run the Server

```cmd
cd D:\codeing\web_control
python main.py
```

The terminal will show:

```
  Local:    http://localhost:5000
  Network:  http://192.168.0.117:5000
```

Open the **Network** URL on any device connected to the same Wi-Fi.

---

## 🔁 Auto-Start on Windows Boot

To make the server start automatically and silently every time Windows starts:

### Step 1 — Edit `start_remote.bat`

Make sure these paths match your system:

```bat
@echo off
cd /d "D:\codeing\web_control"
start "" "C:\Users\YourUsername\AppData\Local\Programs\Python\Python310\pythonw.exe" "D:\codeing\web_control\main.py"
exit
```

> `pythonw.exe` runs the server silently in the background — no terminal window.

### Step 2 — Open the Startup Folder

Press **`Win + R`**, type the following, and press **Enter**:

```
shell:startup
```

### Step 3 — Place the `.bat` File

Copy `start_remote.bat` into the Startup folder. Done — the server will now start automatically on every boot.

---

## 🌐 Accessing the Controller

| Device | URL |
|---|---|
| Same PC | `http://localhost:5000` |
| Phone / Tablet / Other PC | `http://<PC-LOCAL-IP>:5000` |

> To find your PC's local IP, open Command Prompt and type `ipconfig`. Look for **IPv4 Address** under your active network adapter.

---

## 🔐 Logging In

When you open the URL on any device, you'll see the login page. Enter your username and password. After a successful login, you'll be taken to the control panel.

All login attempts (successful and failed) are printed in the server terminal.

---

## 🖱️ How to Use

| Action | How |
|---|---|
| **Left Click** | Single click on the screen canvas |
| **Right Click** | Right-click on the screen canvas |
| **Double Click** | Double-click on the screen canvas |
| **Type Text** | Enter text in the input box → click **Send Text** or press **Enter** |
| **Start Streaming** | Click **Start Streaming** to begin live view |
| **Stop Streaming** | Click **Stop Streaming** to pause |
| **Screenshot** | Click **Single Screenshot** for a one-time capture |
| **Sleep** | System Controls → 💤 Sleep (confirmation required) |
| **Restart** | System Controls → 🔄 Restart (confirmation required) |
| **Shutdown** | System Controls → ⚡ Shutdown (confirmation required) |
| **Logout** | Click the **Logout** button in the top-right corner |

---

## ⚙️ Configuration Reference

All settings are in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `PORT` | `5000` | Server port |
| `SECRET_KEY` | *(change this)* | Flask session encryption key |
| `USERNAME` | `admin` | Login username |
| `PASSWORD_HASH` | `admin123` hashed | Login password |
| `FPS` | `60` | Streaming frame rate |
| `CAPTURE_WIDTH` | `1280` | Stream resolution width |
| `CAPTURE_HEIGHT` | `720` | Stream resolution height |
| `JPEG_QUALITY` | `60` | Image compression (1–95) |
| `DEBUG` | `False` | Flask debug mode |

---

## 🛑 Stopping the Server

**If running in terminal:** Press `Ctrl + C`

**If running silently via `.bat` (auto-start):**
1. Press `Ctrl + Shift + Esc` to open Task Manager
2. Find `pythonw.exe` under Background Processes
3. Right-click → **End Task**

---

## 🔧 Troubleshooting

**Showing "Disconnected" on mobile?**
- Make sure both devices are on the same Wi-Fi network
- Verify `manage_session=False` is set in `server.py`
- Verify `withCredentials: true` is set in `static/app.js`
- Try opening the URL in a different browser

**`TemplateNotFound: login.html` error?**
- Make sure `login.html` and `index.html` are inside a `templates/` folder
- Make sure `app.js` is inside a `static/` folder

**Screen not capturing?**
- Run the server as Administrator on Windows
- Make sure `mss` and `pillow` are installed

**Low FPS?**
- Lower `CAPTURE_WIDTH` and `CAPTURE_HEIGHT` in `config.py`
- Lower `JPEG_QUALITY` for faster encoding

---

## ⚠️ Security Warning

- This tool gives **full control** of your PC to anyone who accesses it
- **Always change** the default username and password before use
- Only use on **trusted private networks** — never expose port `5000` to the internet
- Power actions (Restart/Shutdown) require confirmation but execute quickly — use with care
- All login attempts and system actions are logged in the server terminal

---

## 📜 License

This project is open source and free to use for personal and educational purposes.
