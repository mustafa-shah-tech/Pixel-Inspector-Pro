"""
Pixel Inspector Pro
ui/dashboard.py
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QTextEdit,
    QPushButton,
)

from ui.widgets import Card, InfoRow, ScoreWidget


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.score = ScoreWidget()
        layout.addWidget(self.score)

        grid = QGridLayout()
        layout.addLayout(grid)

        # Device
        self.device_card = Card("Device")
        self.device_layout = QVBoxLayout()
        self.device_card.layout.addLayout(self.device_layout)

        # Battery
        self.battery_card = Card("Battery")
        self.battery_layout = QVBoxLayout()
        self.battery_card.layout.addLayout(self.battery_layout)

        # Display
        self.display_card = Card("Display")
        self.display_layout = QVBoxLayout()
        self.display_card.layout.addLayout(self.display_layout)

        # CPU
        self.cpu_card = Card("CPU")
        self.cpu_layout = QVBoxLayout()
        self.cpu_card.layout.addLayout(self.cpu_layout)

        # Storage
        self.storage_card = Card("Storage")
        self.storage_layout = QVBoxLayout()
        self.storage_card.layout.addLayout(self.storage_layout)

        # Security
        self.security_card = Card("Security")
        self.security_layout = QVBoxLayout()
        self.security_card.layout.addLayout(self.security_layout)

        grid.addWidget(self.device_card, 0, 0)
        grid.addWidget(self.battery_card, 0, 1)
        grid.addWidget(self.display_card, 1, 0)
        grid.addWidget(self.cpu_card, 1, 1)
        grid.addWidget(self.storage_card, 2, 0)
        grid.addWidget(self.security_card, 2, 1)

        self.recommendation = QTextEdit()
        self.recommendation.setReadOnly(True)
        self.recommendation.setMinimumHeight(120)

        layout.addWidget(QLabel("Inspection Summary"))
        layout.addWidget(self.recommendation)

        # Action Buttons

        self.scan_button = QPushButton("Start Inspection")
        self.scan_button.setMinimumHeight(45)

        layout.addWidget(self.scan_button)

    def clear_layout(self, layout):

        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def update_dashboard(self, result):

        self.score.update_score(result.score)

        self.clear_layout(self.device_layout)
        self.clear_layout(self.battery_layout)
        self.clear_layout(self.display_layout)
        self.clear_layout(self.cpu_layout)
        self.clear_layout(self.storage_layout)
        self.clear_layout(self.security_layout)

        # Device

        self.device_layout.addWidget(
            InfoRow("Model", result.device.model)
        )

        self.device_layout.addWidget(
            InfoRow("Android", result.device.android_version)
        )

        self.device_layout.addWidget(
            InfoRow("Build", result.device.build_fingerprint)
        )

        # Battery

        self.battery_layout.addWidget(
            InfoRow("Level", f"{result.battery.level}%")
        )

        self.battery_layout.addWidget(
            InfoRow("Health", result.battery.health)
        )

        self.battery_layout.addWidget(
            InfoRow("Temp", f"{result.battery.temperature} °C")
        )

        # Display

        self.display_layout.addWidget(
            InfoRow("Resolution", result.display.resolution)
        )

        self.display_layout.addWidget(
            InfoRow("Refresh", f"{result.display.refresh_rate} Hz")
        )

        # CPU

        self.cpu_layout.addWidget(
            InfoRow("CPU", result.cpu.processor)
        )

        self.cpu_layout.addWidget(
            InfoRow("RAM", f"{result.cpu.total_ram_gb} GB")
        )

        # Storage

        self.storage_layout.addWidget(
            InfoRow("Total", f"{result.storage.total_gb} GB")
        )

        self.storage_layout.addWidget(
            InfoRow("Free", f"{result.storage.free_gb} GB")
        )

        # Security

        self.security_layout.addWidget(
            InfoRow(
                "Bootloader",
                "Locked" if result.security.bootloader_locked else "Unlocked"
            )
        )

        self.security_layout.addWidget(
            InfoRow(
                "Root",
                "Yes" if result.security.rooted else "No"
            )
        )

        summary = []

        summary.append(
            f"Overall Score: {result.score.total_score}/100"
        )

        summary.append(
            f"Grade: {result.score.grade}"
        )

        summary.append(
            f"Recommendation: {result.score.recommendation}"
        )

        summary.append("")

        if result.score.deductions:

            summary.append("Issues Found:")

            for issue in result.score.deductions:
                summary.append(f"• {issue}")

        else:

            summary.append(
                "No issues detected."
            )

        self.recommendation.setPlainText(
            "\n".join(summary)
        )