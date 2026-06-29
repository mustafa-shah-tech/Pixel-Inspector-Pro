"""
Pixel Inspector Pro
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
)

from PySide6.QtCore import Qt


class Card(QFrame):

    def __init__(self, title="", parent=None):
        super().__init__(parent)

        self.setObjectName("Card")

        self.setFrameShape(QFrame.StyledPanel)

        self.layout = QVBoxLayout(self)

        self.title = QLabel(title)
        self.title.setObjectName("CardTitle")

        self.layout.addWidget(self.title)

        self.layout.setSpacing(10)


class InfoRow(QWidget):

    def __init__(self, key, value):
        super().__init__()

        layout = QHBoxLayout(self)

        self.key = QLabel(key)
        self.key.setMinimumWidth(180)

        self.value = QLabel(str(value))
        self.value.setAlignment(Qt.AlignRight)

        layout.addWidget(self.key)
        layout.addStretch()
        layout.addWidget(self.value)


class ScoreWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.title = QLabel("Overall Score")
        self.title.setAlignment(Qt.AlignCenter)

        self.score = QLabel("--")
        self.score.setAlignment(Qt.AlignCenter)

        self.score.setStyleSheet("""
            font-size:42px;
            font-weight:bold;
            color:#2ecc71;
        """)

        self.grade = QLabel("-")
        self.grade.setAlignment(Qt.AlignCenter)

        self.bar = QProgressBar()
        self.bar.setMaximum(100)

        layout.addWidget(self.title)
        layout.addWidget(self.score)
        layout.addWidget(self.grade)
        layout.addWidget(self.bar)

    def update_score(self, score):

        self.score.setText(str(score.total_score))
        self.grade.setText(
            f"{score.grade} - {score.recommendation}"
        )

        self.bar.setValue(score.total_score)


class StatusBadge(QLabel):

    COLORS = {
        "PASS": "#2ecc71",
        "WARN": "#f39c12",
        "FAIL": "#e74c3c",
        "INFO": "#3498db",
    }

    def __init__(self, text="INFO"):
        super().__init__(text)

        color = self.COLORS.get(text, "#3498db")

        self.setAlignment(Qt.AlignCenter)

        self.setStyleSheet(f"""
            background:{color};
            color:white;
            padding:4px 10px;
            border-radius:8px;
            font-weight:bold;
        """)


class PrimaryButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)

        self.setMinimumHeight(40)

        self.setStyleSheet("""
            QPushButton{
                background:#0A84FF;
                color:white;
                border:none;
                border-radius:8px;
                font-size:14px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#006BE6;
            }

            QPushButton:pressed{
                background:#0054B4;
            }
        """)