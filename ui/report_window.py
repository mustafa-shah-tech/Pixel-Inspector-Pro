"""
Pixel Inspector Pro
ui/report_window.py
"""

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)

from PySide6.QtGui import QDesktopServices

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    WEB_ENGINE_AVAILABLE = True
except Exception:
    WEB_ENGINE_AVAILABLE = False

    from PySide6.QtWidgets import QTextBrowser


class ReportWindow(QMainWindow):

    def __init__(self, report_path: str):
        super().__init__()

        self.report_path = Path(report_path)

        self.setWindowTitle("Inspection Report")
        self.resize(1100, 800)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        if WEB_ENGINE_AVAILABLE:

            self.viewer = QWebEngineView()

            if self.report_path.exists():
                self.viewer.load(
                    QUrl.fromLocalFile(
                        str(self.report_path.resolve())
                    )
                )

        else:

            self.viewer = QTextBrowser()

            if self.report_path.exists():
                self.viewer.setHtml(
                    self.report_path.read_text(
                        encoding="utf-8"
                    )
                )

        layout.addWidget(self.viewer)

        self.open_button = QPushButton("Open in Browser")
        self.save_button = QPushButton("Save Copy")

        self.open_button.clicked.connect(self.open_browser)
        self.save_button.clicked.connect(self.save_copy)

        layout.addWidget(self.open_button)
        layout.addWidget(self.save_button)

    def open_browser(self):

        if self.report_path.exists():

            QDesktopServices.openUrl(
                QUrl.fromLocalFile(
                    str(self.report_path.resolve())
                )
            )

    def save_copy(self):

        if not self.report_path.exists():
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report",
            self.report_path.name,
            "HTML (*.html)"
        )

        if not filename:
            return

        Path(filename).write_text(
            self.report_path.read_text(
                encoding="utf-8"
            ),
            encoding="utf-8"
        )

        QMessageBox.information(
            self,
            "Saved",
            "Report saved successfully."
        )