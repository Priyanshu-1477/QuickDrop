# 📦 QuickDrop

A magical drag-and-drop file sharing app that instantly shares files via QR or link — either on your local network or globally with a public URL (via ngrok).

![QuickDrop Demo](https://your-demo-link.com/demo.gif)

---

## 🚀 Features

* 📁 Drag-and-drop any file to share instantly
* 🌐 Local + Public link generation (with QR)
* ⏳ Auto-expiry (stop sharing when GUI exits)
* 🔊 Sound notification when file is downloaded
* 🧠 Built with Python, Flask, PyQt5, qrcode, pyngrok

---

## 🛠 Tech Stack

* Python 3.10+
* Flask (for the backend server)
* PyQt5 (for GUI)
* qrcode + Pillow (for QR image generation)
* pyngrok (for public internet link)
* pyperclip (copy to clipboard)
* playsound (for download notification)

---

## 📦 Installation

```bash
pip install flask pyqt5 qrcode[pil] pyngrok pyperclip playsound
```

```bash
git clone https://github.com/Priyanshu-1477/QuickDrop.git
cd QuickDrop
```

👉 You also need:

* [ngrok account](https://dashboard.ngrok.com/signup)
* Set your authtoken:
  `ngrok config add-authtoken <your_token>`

---

## 🔄 Usage

### GUI Mode (Recommended)

```bash
QT_QPA_PLATFORM=xcb python3 gui.py
```

* Just drag a file into the window
* It will generate a local and public share link + QR
* QR appears in the GUI; link is copied to clipboard

### CLI Mode (Manual)

```bash
python3 app.py <path-to-your-file>
```

This will:

* Start a local server at `http://<LAN_IP>:5000/download`
* Create a public ngrok tunnel `https://xyz.ngrok-free.app/download`

---

## 🌐 Access Modes

| Mode   | Use Case              | Access URL                              |
| ------ | --------------------- | --------------------------------------- |
| Local  | Same Wi-Fi or Hotspot | `http://192.168.x.x:5000/download`      |
| Public | Internet access       | `https://xxxxx.ngrok-free.app/download` |

---

## 🧪 Test It

* Connect another device (mobile/laptop) to same network
* Open the local or public link
* Download the file
* Hear the 🔊 sound on sender’s machine

---

## 🧼 Clean Exit

Press `ENTER` in terminal or close GUI window to stop sharing.

---

## 📌 Notes

* PyQt GUI auto-copies the public URL to clipboard
* Only one file is shared at a time
* Downloading triggers a sound notification
* Auto handles port binding and QR display

---

## 🤝 Contributing

Pull requests are welcome! Ideas for improvements:

* Multiple file sharing
* File preview before download
* Password protection

---

## 🧑‍💻 Author

Priyanshu Raj

Made with ❤️ using Python and caffeine ☕

---

## 📃 License

[MIT License](LICENSE)
