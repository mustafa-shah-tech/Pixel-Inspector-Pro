"""
Pixel Inspector Pro
core/utils.py

Common utility functions used throughout the application.
"""

from __future__ import annotations

import platform
import shutil
from pathlib import Path
from datetime import datetime


# -------------------------------------------------------------------
# General
# -------------------------------------------------------------------

APP_NAME = "Pixel Inspector Pro"
APP_VERSION = "0.1.0"

BASE_DIR = Path(__file__).resolve().parent.parent

REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"
DATABASE_DIR = BASE_DIR / "database"

REPORT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)


# -------------------------------------------------------------------
# Date & Time
# -------------------------------------------------------------------

def current_timestamp() -> str:
    """Return current timestamp."""

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def current_filename_time() -> str:
    """Timestamp suitable for filenames."""

    return datetime.now().strftime("%Y%m%d_%H%M%S")


# -------------------------------------------------------------------
# Platform
# -------------------------------------------------------------------

def operating_system() -> str:
    """Return host operating system."""

    return platform.system()


def is_windows() -> bool:
    return operating_system() == "Windows"


# -------------------------------------------------------------------
# Formatting
# -------------------------------------------------------------------

def bytes_to_gb(size: int) -> float:
    """
    Convert bytes into gigabytes.
    """

    return round(size / (1024 ** 3), 2)


def kb_to_gb(size: int) -> float:
    """
    Convert kilobytes into gigabytes.
    """

    return round(size / (1024 ** 2), 2)


# -------------------------------------------------------------------
# Files
# -------------------------------------------------------------------

def reports_directory() -> Path:
    return REPORT_DIR


def logs_directory() -> Path:
    return LOG_DIR


def database_directory() -> Path:
    return DATABASE_DIR


# -------------------------------------------------------------------
# Executables
# -------------------------------------------------------------------

def executable_exists(name: str) -> bool:
    """
    Check if an executable exists in PATH.
    """

    return shutil.which(name) is not None


# -------------------------------------------------------------------
# Report Filename
# -------------------------------------------------------------------

def create_report_filename(device_name: str) -> Path:
    """
    Generate report filename.

    Example:
    Pixel_7_Pro_20260629_142511.pdf
    """

    clean = device_name.replace(" ", "_")

    filename = f"{clean}_{current_filename_time()}.pdf"

    return REPORT_DIR / filename


# -------------------------------------------------------------------
# Console Banner
# -------------------------------------------------------------------

def banner() -> str:

    return f"""
===========================================
{APP_NAME}
Version {APP_VERSION}
===========================================
"""