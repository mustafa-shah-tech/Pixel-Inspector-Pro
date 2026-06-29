"""
Pixel Inspector Pro
ui/settings.py
"""

from pathlib import Path
import json

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QComboBox,
    QMessageBox,
)

CONFIG_FILE = Path("settings.json")


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.resize(420, 320)

        layout = QVBoxLayout(self)

        # Theme
        layout.addWidget(QLabel("Theme"))

        self.theme = QComboBox()
        self.theme.addItems([
            "Dark",
            "Light",
        ])

        layout.addWidget(self.theme)

        # Reports

        self.open_report = QCheckBox(
            "Open report automatically after inspection"
        )

        self.open_report.setChecked(True)

        layout.addWidget(self.open_report)

        self.save_html = QCheckBox(
            "Generate HTML Report"
        )

        self.save_html.setChecked(True)

        layout.addWidget(self.save_html)

        self.save_json = QCheckBox(
            "Generate JSON Report (Future)"
        )

        layout.addWidget(self.save_json)

        self.save_pdf = QCheckBox(
            "Generate PDF Report (Future)"
        )

        layout.addWidget(self.save_pdf)

        layout.addStretch()

        buttons = QHBoxLayout()

        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")

        buttons.addStretch()
        buttons.addWidget(self.cancel_btn)
        buttons.addWidget(self.save_btn)

        layout.addLayout(buttons)

        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn.clicked.connect(self.close)

        self.load_settings()

    def load_settings(self):

        if not CONFIG_FILE.exists():
            return

        try:

            data = json.loads(
                CONFIG_FILE.read_text(
                    encoding="utf-8"
                )
            )

            self.theme.setCurrentText(
                data.get("theme", "Dark")
            )

            self.open_report.setChecked(
                data.get("open_report", True)
            )

            self.save_html.setChecked(
                data.get("save_html", True)
            )

            self.save_json.setChecked(
                data.get("save_json", False)
            )

            self.save_pdf.setChecked(
                data.get("save_pdf", False)
            )

        except Exception:
            pass

    def save_settings(self):

        data = {

            "theme": self.theme.currentText(),

            "open_report": self.open_report.isChecked(),

            "save_html": self.save_html.isChecked(),

            "save_json": self.save_json.isChecked(),

            "save_pdf": self.save_pdf.isChecked(),

        }

        CONFIG_FILE.write_text(
            json.dumps(
                data,
                indent=4
            ),
            encoding="utf-8"
        )

        QMessageBox.information(
            self,
            "Saved",
            "Settings saved successfully."
        )

        self.accept()