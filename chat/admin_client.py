import sys
import asyncio

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QTextEdit, QWidget


class AdminApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(200, 200, 500, 400)

        # Интерфейс
        self.layout = QVBoxLayout()
        self.message_box = QTextEdit()
        self.message_box.setReadOnly(True)
        self.layout.addWidget(self.message_box)
        self.setLayout(self.layout)

        # Запускаем WebSocket в asyncio
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.listen_to_websocket())

    async def listen_to_websocket(self):
        uri = "ws://127.0.0.1:8000/ws/admin/"
        async with websockets.connect(uri) as websocket:
            self.message_box.append("Connected to WebSocket as Admin...\n")

            while True:
                # Получаем новые сообщения от WebSocket
                message = await websocket.recv()
                self.message_box.append(f"New Event: {message}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    admin_panel = AdminApp()
    admin_panel.show()
    sys.exit(app.exec())