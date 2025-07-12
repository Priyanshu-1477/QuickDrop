# gui.py

import sys
import os
import subprocess
import qrcode
import threading
import pyperclip
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class DropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📦 QuickDrop – Drag & Share")
        self.setGeometry(100, 100, 400, 600)
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.instruction = QLabel("➡️ Drag a file into this window")
        self.instruction.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.instruction)

        self.qr1_label = QLabel()
        self.qr2_label = QLabel()
        self.link1_button = QPushButton("📋 Copy Local Link")
        self.link2_button = QPushButton("📋 Copy Public Link")

        self.layout.addWidget(self.qr1_label)
        self.layout.addWidget(self.link1_button)
        self.layout.addWidget(self.qr2_label)
        self.layout.addWidget(self.link2_button)

        self.link1_button.clicked.connect(self.copy_local)
        self.link2_button.clicked.connect(self.copy_public)

        self.local_link = ""
        self.public_link = ""

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return

        file_path = urls[0].toLocalFile()
        if not os.path.isfile(file_path):
            return

        self.instruction.setText("⏳ Uploading and generating links...")

        thread = threading.Thread(target=self.share_file, args=(file_path,))
        thread.start()

    def share_file(self, file_path):
        process = subprocess.Popen(
            ["python3", "app.py", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            if "🖧 Local link:" in line:
                self.local_link = line.strip().split(":", 1)[1].strip()
                self.update_qr(self.qr1_label, self.local_link)

            elif "✅ Public link:" in line:
                self.public_link = line.strip().split(":", 1)[1].strip()
                self.update_qr(self.qr2_label, self.public_link)

        self.instruction.setText("✅ File is ready to share!")

    def update_qr(self, label_widget, data):
        qr = qrcode.make(data)
        qr = qr.resize((200, 200))
        img = qr.convert("RGB")

        image = QImage(img.tobytes(), img.size[0], img.size[1], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        label_widget.setPixmap(pixmap)
        label_widget.setAlignment(Qt.AlignCenter)

    def copy_local(self):
        if self.local_link:
            pyperclip.copy(self.local_link)

    def copy_public(self):
        if self.public_link:
            pyperclip.copy(self.public_link)


def run_gui():
    app = QApplication(sys.argv)
    window = DropWidget()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
