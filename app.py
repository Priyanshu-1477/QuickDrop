# app.py

import os
import sys
import threading
import time
import socket
from flask import Flask, send_from_directory
from pyngrok import ngrok
from playsound import playsound

app = Flask(__name__)
shared_file_path = None


@app.route("/")
def index():
    return "<h2>🚫 No file shared yet. Drag a file into QuickDrop.</h2>"


@app.route("/download")
def download_file():
    global shared_file_path
    if not shared_file_path or not os.path.exists(shared_file_path):
        return "⚠️ No file available to download."

    folder = os.path.dirname(shared_file_path)
    filename = os.path.basename(shared_file_path)

    # Sound for download
    threading.Thread(target=playsound, args=("ding.mp3",), daemon=True).start()
    return send_from_directory(folder, filename, as_attachment=True)


def get_local_ip():
    """Find your LAN IP"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def run_flask():
    app.run(host="0.0.0.0", port=5000)


def run_server(file_path):
    global shared_file_path

    shared_file_path = file_path
    print(f"🚀 File set: {shared_file_path}")

    # Start Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    time.sleep(2)

    # Local link (LAN)
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:5000/download"
    print(f"🖧 Local link: {local_url}")

    # Public ngrok tunnel
    print("🌍 Tunneling via ngrok...")
    tunnel = ngrok.connect(5000)
    public_url = tunnel.public_url
    print(f"✅ Public link: {public_url}/download")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python3 app.py <file_to_share>")
        sys.exit(1)

    file_to_share = sys.argv[1]
    if not os.path.exists(file_to_share):
        print("❌ File does not exist:", file_to_share)
        sys.exit(1)

    run_server(file_to_share)
    input("⏳ Press Enter to stop sharing...\n")
