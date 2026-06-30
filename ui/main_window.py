"""
Pixel Inspector Pro
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

        self.setWindowTitle("Pixel Inspector Pro")
        self.resize(1200, 750)

        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)

        self._thread = None   # QThread kept alive during scan

        self.manager = None

        try:
            self.manager = Inspector()
        except Exception as e:
            QMessageBox.warning(
                self,
                "ADB",
                str(e),
            )

        self.dashboard.scan_button.clicked.connect(
            self.scan_device
        )

        self.statusBar().showMessage("Ready")

    # ------------------------------------------------------------------
    # Slot: Start Inspection button
    # ------------------------------------------------------------------

    def scan_device(self):

        if self.manager is None:
            QMessageBox.warning(
                self,
                "ADB",
                "ADB was not found.",
            )
            return

        if not self.manager.is_connected():
            QMessageBox.information(
                self,
                "No Device",
                "No Android device detected.\n\n"
                "Enable USB Debugging and reconnect.",
            )
            return

        # Lock the button and show status while running
        self.dashboard.scan_button.setEnabled(False)
        self.statusBar().showMessage("Scanning…")

        # Build worker + thread
        self._thread = QThread(self)
        self._worker = _InspectWorker(self.manager)
        self._worker.moveToThread(self._thread)

        # Wire signals
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_inspect_done)
        self._worker.error.connect(self._on_inspect_error)

        # Clean up the thread when the worker signals are done
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()

    # ------------------------------------------------------------------
    # Worker callbacks (main thread)
    # ------------------------------------------------------------------

    def _on_inspect_done(self, result):
        self.dashboard.update_dashboard(result)
        self.statusBar().showMessage(
            f"Inspection complete — {result.device.model}"
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