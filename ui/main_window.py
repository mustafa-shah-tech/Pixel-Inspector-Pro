"""
Android Inspector Pro
ui/main_window.py
"""

from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from ui.dashboard import Dashboard
from core.inspector import Inspector


# ---------------------------------------------------------------------------
# Background worker
# ---------------------------------------------------------------------------

class _InspectWorker(QObject):
    """Runs Inspector.inspect() on a background thread."""

    finished = Signal(object)   # emits InspectionResult on success
    error = Signal(str)         # emits error message on failure

    def __init__(self, manager: Inspector):
        super().__init__()
        self._manager = manager

    def run(self):
        try:
            result = self._manager.inspect()
            self.finished.emit(result)
        except Exception as exc:
            self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Android Inspector Pro")
        self.setMinimumSize(1280, 800)
        self.resize(1280, 800)

        self.setStyleSheet("QMainWindow { background: #0D0D0F; }")

        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)

        self._thread = None

        self.manager = None

        try:
            self.manager = Inspector()
        except Exception as e:
            QMessageBox.warning(self, "ADB", str(e))

        self.dashboard.scan_button.clicked.connect(self.scan_device)

        self.statusBar().showMessage("Ready")

    # ------------------------------------------------------------------

    def scan_device(self):

        if self.manager is None:
            QMessageBox.warning(self, "ADB", "ADB was not found.")
            return

        if not self.manager.is_connected():
            QMessageBox.information(
                self,
                "No Device",
                "No Android device detected.\n\nEnable USB Debugging and reconnect.",
            )
            return

        self.dashboard.scan_button.setEnabled(False)
        self.statusBar().showMessage("Scanning…")

        self._thread = QThread(self)
        self._worker = _InspectWorker(self.manager)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_inspect_done)
        self._worker.error.connect(self._on_inspect_error)

        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    # ------------------------------------------------------------------

    def _on_inspect_done(self, result):
        self.dashboard.update_dashboard(result)
        self.statusBar().showMessage(
            f"✓  Inspection complete — {result.device.model}"
        )
        self._reset_ui()

    def _on_inspect_error(self, message: str):
        QMessageBox.warning(
            self,
            "Inspection Error",
            f"Scan failed:\n\n{message}",
        )
        self.statusBar().showMessage("Ready")
        self._reset_ui()

    def _reset_ui(self):
        self.dashboard.scan_button.setEnabled(True)