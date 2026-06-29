"""
Pixel Inspector Pro
ui/main_window.py
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from ui.dashboard import Dashboard
from core.device import DeviceManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pixel Inspector Pro")
        self.resize(1200, 750)

        self.dashboard = Dashboard()

        self.setCentralWidget(self.dashboard)

        self.manager = None

        try:
            self.manager = DeviceManager()
        except Exception as e:
            QMessageBox.warning(
                self,
                "ADB",
                str(e),
            )

        self.dashboard.scan_button.clicked.connect(
            self.scan_device
        )

        self.statusBar().showMessage(
            "Ready"
        )

    def scan_device(self):

        if self.manager is None:
            QMessageBox.warning(
                self,
                "ADB",
                "ADB was not found."
            )
            return

        if not self.manager.is_connected():
            QMessageBox.information(
                self,
                "No Device",
                "No Android device detected.\n\n"
                "Enable USB Debugging and reconnect."
            )
            return

        device = self.manager.get_device()

        self.dashboard.update_device(device)

        self.statusBar().showMessage(
            f"{device.model} connected"
        )