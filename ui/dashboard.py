"""
Android Inspector Pro
ui/dashboard.py
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QTextEdit,
    QFrame,
    QScrollArea,
    QSizePolicy,
)

from PySide6.QtCore import Qt

from ui.widgets import Card, InfoRow, ScoreWidget, PrimaryButton


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background: #0D0D0F;")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ----------------------------------------------------------------
        # Header bar
        # ----------------------------------------------------------------

        header = QFrame()
        header.setFixedHeight(64)
        header.setFrameShape(QFrame.NoFrame)
        header.setStyleSheet("""
            QFrame {
                background: #13131A;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            }
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)
        header_layout.setSpacing(10)

        icon_label = QLabel("🔍")
        icon_label.setStyleSheet("""
            font-size: 22px;
            background: transparent;
            border: none;
        """)

        app_name_label = QLabel("Android Inspector Pro")
        app_name_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #F5F5F7;
            background: transparent;
            border: none;
        """)

        self.scan_button = PrimaryButton("Start Inspection")
        self.scan_button.setFixedWidth(180)

        header_layout.addWidget(icon_label)
        header_layout.addWidget(app_name_label)
        header_layout.addStretch()
        header_layout.addWidget(self.scan_button)

        root.addWidget(header)

        # ----------------------------------------------------------------
        # Scrollable content area
        # ----------------------------------------------------------------

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent;")

        content = QWidget()
        content.setStyleSheet("background: transparent;")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(16)

        # Score widget (full-width)
        self.score = ScoreWidget()
        content_layout.addWidget(self.score)

        # Grid of cards
        grid = QGridLayout()
        grid.setSpacing(16)
        grid.setContentsMargins(0, 0, 0, 0)

        # Device
        self.device_card = Card("Device")
        self.device_layout = QVBoxLayout()
        self.device_layout.setSpacing(0)
        self.device_card.layout.addLayout(self.device_layout)

        # Battery
        self.battery_card = Card("Battery")
        self.battery_layout = QVBoxLayout()
        self.battery_layout.setSpacing(0)
        self.battery_card.layout.addLayout(self.battery_layout)

        # Display
        self.display_card = Card("Display")
        self.display_layout = QVBoxLayout()
        self.display_layout.setSpacing(0)
        self.display_card.layout.addLayout(self.display_layout)

        # CPU
        self.cpu_card = Card("CPU & Memory")
        self.cpu_layout = QVBoxLayout()
        self.cpu_layout.setSpacing(0)
        self.cpu_card.layout.addLayout(self.cpu_layout)

        # Storage
        self.storage_card = Card("Storage")
        self.storage_layout = QVBoxLayout()
        self.storage_layout.setSpacing(0)
        self.storage_card.layout.addLayout(self.storage_layout)

        # Security
        self.security_card = Card("Security")
        self.security_layout = QVBoxLayout()
        self.security_layout.setSpacing(0)
        self.security_card.layout.addLayout(self.security_layout)

        # Software
        self.software_card = Card("Software")
        self.software_layout = QVBoxLayout()
        self.software_layout.setSpacing(0)
        self.software_card.layout.addLayout(self.software_layout)

        grid.addWidget(self.device_card,   0, 0)
        grid.addWidget(self.battery_card,  0, 1)
        grid.addWidget(self.display_card,  1, 0)
        grid.addWidget(self.cpu_card,      1, 1)
        grid.addWidget(self.storage_card,  2, 0)
        grid.addWidget(self.security_card, 2, 1)
        grid.addWidget(self.software_card, 3, 0)

        content_layout.addLayout(grid)

        # Inspection summary
        summary_label = QLabel("INSPECTION SUMMARY")
        summary_label.setStyleSheet("""
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.8px;
            color: rgba(245, 245, 247, 0.45);
            background: transparent;
            border: none;
        """)
        content_layout.addWidget(summary_label)

        self.recommendation = QTextEdit()
        self.recommendation.setReadOnly(True)
        self.recommendation.setMinimumHeight(120)
        self.recommendation.setMaximumHeight(180)
        self.recommendation.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-top: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 14px;
                padding: 12px 16px;
                color: rgba(245, 245, 247, 0.75);
                font-size: 13px;
            }
        """)
        content_layout.addWidget(self.recommendation)

        scroll.setWidget(content)
        root.addWidget(scroll)

    # ------------------------------------------------------------------

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
        self.clear_layout(self.software_layout)

        # Device

        self.device_layout.addWidget(InfoRow("Model", result.device.model))
        self.device_layout.addWidget(InfoRow("Android", result.device.android_version))
        self.device_layout.addWidget(InfoRow("Build", result.device.build_fingerprint))
        self.device_layout.addWidget(InfoRow("Build Date", result.device.build_date or "Unknown"))
        self.device_layout.addWidget(InfoRow("Kernel", result.device.kernel_version or "Unknown"))
        self.device_layout.addWidget(InfoRow("Bootloader", result.device.bootloader_version or "Unknown"))

        # Battery

        self.battery_layout.addWidget(InfoRow("Level", f"{result.battery.level}%"))
        self.battery_layout.addWidget(InfoRow("Health", result.battery.health))
        self.battery_layout.addWidget(InfoRow("Temp", f"{result.battery.temperature} °C"))
        self.battery_layout.addWidget(InfoRow("Charging", result.battery.charging_type))
        self.battery_layout.addWidget(InfoRow("Score", f"{result.battery.battery_score}/100"))

        # Display

        self.display_layout.addWidget(InfoRow("Resolution", result.display.resolution))
        self.display_layout.addWidget(InfoRow("Refresh", f"{result.display.refresh_rate} Hz"))
        self.display_layout.addWidget(
            InfoRow(
                "Diagonal",
                f"{result.display.diagonal_inches} in"
                if result.display.diagonal_inches is not None
                else "Unknown"
            )
        )
        self.display_layout.addWidget(InfoRow("Color Space", result.display.color_space))
        self.display_layout.addWidget(InfoRow("OLED", "Yes" if result.display.oled_verified else "No"))

        # CPU

        self.cpu_layout.addWidget(InfoRow("CPU", result.cpu.processor))
        self.cpu_layout.addWidget(InfoRow("RAM", f"{result.cpu.total_ram_gb} GB"))
        self.cpu_layout.addWidget(InfoRow("Governor", result.cpu.governor or "Unknown"))
        self.cpu_layout.addWidget(InfoRow("GPU", result.cpu.gpu_model or "Unknown"))
        self.cpu_layout.addWidget(InfoRow("Thermal", result.cpu.thermal_status))

        # Storage

        self.storage_layout.addWidget(InfoRow("Total", f"{result.storage.total_gb} GB"))
        self.storage_layout.addWidget(InfoRow("Free", f"{result.storage.free_gb} GB"))

        # Security

        self.security_layout.addWidget(
            InfoRow("Bootloader", "Locked" if result.security.bootloader_locked else "Unlocked")
        )
        self.security_layout.addWidget(
            InfoRow("Root", "Yes" if result.security.rooted else "No")
        )

        # Software

        self.software_layout.addWidget(InfoRow("Installed Apps", str(result.software.installed_apps_count)))
        self.software_layout.addWidget(InfoRow("System Apps", str(result.software.system_apps_count)))
        self.software_layout.addWidget(InfoRow("Play Services", result.software.play_services_version))
        self.software_layout.addWidget(
            InfoRow("Play Protect", "Enabled" if result.software.play_protect_enabled else "Disabled")
        )
        self.software_layout.addWidget(InfoRow("Update Status", result.software.update_status))

        # Summary text

        summary = []
        summary.append(f"Overall Score: {result.score.total_score}/100")
        summary.append(f"Grade: {result.score.grade}")
        summary.append(f"Recommendation: {result.score.recommendation}")

        brand_label = {
            "pixel":   "Google Pixel",
            "samsung": "Samsung",
            "generic": "Android (Generic)",
        }.get(result.brand, result.brand.title())

        summary.append(f"Brand: {brand_label}")

        if hasattr(result.brand_result, "authenticity_score"):
            summary.append(f"Authenticity Score: {result.brand_result.authenticity_score}/100")

        summary.append("")

        if result.score.deductions:
            summary.append("Issues Found:")
            for issue in result.score.deductions:
                summary.append(f"  •  {issue}")
        else:
            summary.append("No issues detected.")

        self.recommendation.setPlainText("\n".join(summary))