"""
Android Inspector Pro
ui/widgets.py
"""

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QProgressBar,
    QSizePolicy,
)

from PySide6.QtCore import Qt


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------

class Card(QFrame):

    def __init__(self, title="", parent=None):
        super().__init__(parent)

        self.setObjectName("Card")
        self.setFrameShape(QFrame.NoFrame)

        self.setStyleSheet("""
            QFrame#Card {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-top: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 16px;
                padding: 8px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(14, 12, 14, 12)
        self.layout.setSpacing(4)

        self.title_label = QLabel(title.upper())
        self.title_label.setObjectName("CardTitle")
        self.title_label.setStyleSheet("""
            QLabel#CardTitle {
                font-size: 11px;
                font-weight: 600;
                letter-spacing: 0.8px;
                color: rgba(245, 245, 247, 0.45);
                padding-bottom: 6px;
                border: none;
                background: transparent;
            }
        """)

        self.layout.addWidget(self.title_label)


# ---------------------------------------------------------------------------
# InfoRow
# ---------------------------------------------------------------------------

class InfoRow(QWidget):

    def __init__(self, key, value):
        super().__init__()

        self.setFixedHeight(28)
        self.setStyleSheet("""
            QWidget {
                border-bottom: 1px solid rgba(255, 255, 255, 0.04);
                background: transparent;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.key = QLabel(key)
        self.key.setMinimumWidth(160)
        self.key.setStyleSheet("""
            font-size: 12px;
            color: rgba(245, 245, 247, 0.5);
            border: none;
            background: transparent;
        """)

        self.value = QLabel(str(value))
        self.value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.value.setStyleSheet("""
            font-size: 12px;
            font-weight: 500;
            color: #F5F5F7;
            border: none;
            background: transparent;
        """)

        layout.addWidget(self.key)
        layout.addWidget(self.value)


# ---------------------------------------------------------------------------
# ScoreWidget
# ---------------------------------------------------------------------------

class ScoreWidget(QWidget):

    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        # Glass frame
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.10);
                border-top: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(6)

        # Label: "OVERALL SCORE"
        self.title = QLabel("OVERALL SCORE")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
            color: rgba(245, 245, 247, 0.45);
            border: none;
            background: transparent;
        """)

        # Score number
        self.score = QLabel("--")
        self.score.setAlignment(Qt.AlignCenter)
        self.score.setStyleSheet("""
            font-size: 64px;
            font-weight: 700;
            color: #F5F5F7;
            border: none;
            background: transparent;
        """)

        # Grade
        self.grade = QLabel("-")
        self.grade.setAlignment(Qt.AlignCenter)
        self.grade.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #0A84FF;
            border: none;
            background: transparent;
        """)

        # Recommendation
        self.recommendation = QLabel("")
        self.recommendation.setAlignment(Qt.AlignCenter)
        self.recommendation.setStyleSheet("""
            font-size: 13px;
            color: rgba(245, 245, 247, 0.55);
            border: none;
            background: transparent;
        """)

        # Progress bar
        self.bar = QProgressBar()
        self.bar.setMaximum(100)
        self.bar.setFixedHeight(8)
        self.bar.setTextVisible(False)

        layout.addWidget(self.title)
        layout.addWidget(self.score)
        layout.addWidget(self.grade)
        layout.addWidget(self.recommendation)
        layout.addSpacing(8)
        layout.addWidget(self.bar)

        outer.addWidget(self.frame)

    def update_score(self, score):

        self.score.setText(str(score.total_score))
        self.grade.setText(score.grade)
        self.recommendation.setText(score.recommendation)
        self.bar.setValue(score.total_score)

        # Dynamic score colour
        s = score.total_score
        if s >= 95:
            color = "#30D158"
        elif s >= 80:
            color = "#0A84FF"
        elif s >= 60:
            color = "#FF9F0A"
        else:
            color = "#FF453A"

        self.score.setStyleSheet(f"""
            font-size: 64px;
            font-weight: 700;
            color: {color};
            border: none;
            background: transparent;
        """)


# ---------------------------------------------------------------------------
# StatusBadge
# ---------------------------------------------------------------------------

class StatusBadge(QLabel):

    _STYLES = {
        "PASS": (
            "rgba(48, 209, 88, 0.15)",
            "#30D158",
            "rgba(48, 209, 88, 0.3)",
        ),
        "WARN": (
            "rgba(255, 159, 10, 0.15)",
            "#FF9F0A",
            "rgba(255, 159, 10, 0.3)",
        ),
        "FAIL": (
            "rgba(255, 69, 58, 0.15)",
            "#FF453A",
            "rgba(255, 69, 58, 0.3)",
        ),
        "INFO": (
            "rgba(10, 132, 255, 0.15)",
            "#0A84FF",
            "rgba(10, 132, 255, 0.3)",
        ),
    }

    def __init__(self, text="INFO"):
        super().__init__(text)

        bg, fg, border = self._STYLES.get(
            text,
            self._STYLES["INFO"],
        )

        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""
            background: {bg};
            color: {fg};
            border: 1px solid {border};
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
        """)


# ---------------------------------------------------------------------------
# PrimaryButton
# ---------------------------------------------------------------------------

class PrimaryButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)

        self.setMinimumHeight(44)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0A84FF, stop:1 #0066CC
                );
                color: #FFFFFF;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 600;
                padding: 0 24px;
            }

            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1A8FFF, stop:1 #0075E0
                );
            }

            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #006BE6, stop:1 #0054B4
                );
            }

            QPushButton:disabled {
                background: rgba(255, 255, 255, 0.08);
                color: rgba(245, 245, 247, 0.3);
            }
        """)