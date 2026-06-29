#!/usr/bin/env python3
"""
Pixel Inspector Pro
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


APP_NAME = "Pixel Inspector Pro"
APP_VERSION = "0.1.0"


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
        logging.FileHandler(LOG_DIR / "pixel_inspector.log", encoding="utf-8"),
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
        f"Pixel Inspector Pro has crashed.\n\n"
        f"A log has been written to:\n\n"
        f"{LOG_DIR / 'pixel_inspector.log'}",
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

    window = MainWindow()
    window.show()

    logger.info("Application started.")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()