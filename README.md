# LAN-Remote-Desktop-Controller
🖥️ Browser-based LAN remote desktop — live screen streaming, mouse &amp; keyboard control, and system power management.

🖥️ LAN Remote Desktop Controller
Browser-based LAN remote desktop tool with live screen streaming, mouse & keyboard control, and system power management.

✨ Features

📺 Live screen streaming up to 60 FPS
🖱️ Mouse control (left click, right click, double click)
⌨️ Keyboard / text input
⚡ System power controls (Sleep, Restart, Shutdown)
🌐 Works from any browser on the same network
🔧 Auto-start on Windows boot


📋 Requirements

Windows 10 / 11
Python 3.10+
The following Python packages:

pip install flask flask-socketio pyautogui mss pillow python-socketio

🚀 Installation & Setup
1. Clone or Download the Project
Place the project folder at:
D:\codeing\web_control\

You can use any path — just update the .bat file accordingly.


2. Install Dependencies
Open Command Prompt and run:
cmdpip install flask flask-socketio pyautogui mss pillow python-socketio

3. Run the Server Manually (Test First)
cmdcd D:\codeing\web_control
python main.py
Then open your browser and go to:
http://localhost:5000
Or from another device on the same Wi-Fi:
http://<YOUR-PC-IP>:5000

Your PC's local IP will be printed in the terminal when the server starts.


🔁 Auto-Start on Windows Boot
To make the server start automatically when Windows starts:
Step 1 — Create the .bat file
Create a file named start_remote.bat with the following content:
bat@echo off
cd /d "D:\codeing\web_control"
start "" "C:\Users\User\AppData\Local\Programs\Python\Python310\pythonw.exe" "D:\codeing\web_control\main.py"
exit

Note: Replace C:\Users\User\ with your actual Windows username path if different.
pythonw.exe is used instead of python.exe so the server runs silently in the background without a terminal window.


Step 2 — Open the Startup Folder

Press Win + R to open the Run dialog
Type the following and press Enter:

shell:startup
This opens the Windows Startup folder:
C:\Users\<YourUsername>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

Step 3 — Place the .bat File
Copy or move start_remote.bat into the Startup folder you just opened.
That's it! The server will now automatically start every time Windows boots, running silently in the background.

🌐 Accessing the Controller
DeviceURLSame PChttp://localhost:5000Phone / Tablet / Other PC on same Wi-Fihttp://<PC-LOCAL-IP>:5000

To find your PC's local IP, open Command Prompt and type ipconfig. Look for the IPv4 Address under your Wi-Fi or Ethernet adapter.


🖱️ How to Use
ActionHowLeft ClickSingle click on the screen canvasRight ClickRight-click on the screen canvasDouble ClickDouble-click on the screen canvasType TextEnter text in the input box → click Send TextStart StreamingClick Start Streaming buttonStop StreamingClick Stop Streaming buttonScreenshotClick Single Screenshot for a one-time captureSleep / Restart / ShutdownUse the System Controls buttons (confirmation required)

⚠️ Security Warning

This tool gives full control of your PC to anyone who accesses it
Only use on trusted private networks
Do not expose port 5000 to the internet
System power controls (Restart/Shutdown) have a built-in delay for safety


🛑 Stopping the Server
Since the server runs silently with pythonw.exe, to stop it:

Press Ctrl + Shift + Esc to open Task Manager
Find pythonw.exe under Background Processes
Right-click → End Task


📁 Project Structure
web_control/
├── main.py            # Main Flask server
├── start_remote.bat   # Windows auto-start batch file
└── README.md          # This file

📜 License
This project is open source and free to use for personal and educational purposes.
