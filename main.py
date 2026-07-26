#!/usr/bin/env python3
"""
Android Inspector Pro
Main Entry Point

Author: Mustafa Shah
License: MIT
"""

from __future__ import annotations

import logging
import os
import pathlib
import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from ui.main_window import MainWindow


APP_NAME = "Android Inspector Pro"
APP_VERSION = "1.1.1"


# ----------------------------------------------------------
# Directories
# ----------------------------------------------------------

BASE_DIR = pathlib.Path(__file__).resolve().parent

REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"
DATABASE_DIR = BASE_DIR / "database"

for directory in (REPORT_DIR, LOG_DIR, DATABASE_DIR):
    directory.mkdir(exist_ok=True)


# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "android_inspector.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------
# Global Exception Handler
# ----------------------------------------------------------

def exception_hook(exc_type, exc_value, exc_traceback):
    """
    Catch unexpected crashes and show a dialog instead of
    silently closing the application.
    """

    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback,
        )
    )

    logger.critical(error)

    QMessageBox.critical(
        None,
        "Unexpected Error",
        f"Android Inspector Pro has crashed.\n\n"
        f"A log has been written to:\n\n"
        f"{LOG_DIR / 'android_inspector.log'}",
    )


sys.excepthook = exception_hook


# ----------------------------------------------------------
# Application
# ----------------------------------------------------------

def main():

    logger.info("=" * 60)
    logger.info("%s %s", APP_NAME, APP_VERSION)
    logger.info("=" * 60)

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("Mustafa Shah Tech")

    app.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #0D0D0F;
            color: #F5F5F7;
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
        }

        QScrollArea, QScrollArea > QWidget > QWidget {
            background: transparent;
        }

        QScrollBar:vertical {
            background: transparent;
            width: 6px;
            margin: 0;
        }
        QScrollBar::handle:vertical {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 3px;
            min-height: 30px;
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }

        QStatusBar {
            background: #13131A;
            color: rgba(245, 245, 247, 0.55);
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            font-size: 12px;
        }

        QMessageBox {
            background: #1C1C1E;
            color: #F5F5F7;
        }

        QProgressBar {
            background: rgba(255, 255, 255, 0.06);
            border: none;
            border-radius: 4px;
            height: 6px;
            text-align: center;
            color: transparent;
        }
        QProgressBar::chunk {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0A84FF, stop:1 #30D158
            );
            border-radius: 4px;
        }
    """)

    window = MainWindow()
    window.show()

    logger.info("Application started.")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()