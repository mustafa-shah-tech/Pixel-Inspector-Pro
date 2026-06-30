"""
Pixel Inspector Pro
core/display.py

Display inspection module.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from core.adb import ADB


@dataclass
class DisplayInfo:
    resolution: str = ""
    density: str = ""
    refresh_rate: float = 0.0

    width: int = 0
    height: int = 0

    orientation: str = "Unknown"

    brightness_mode: str = "Unknown"

    hdr_supported: bool = False

    screen_on: bool = False

    diagonal_inches: float | None = None
    color_space: str = "Unknown"
    oled_verified: bool = False


class DisplayInspector:

    def __init__(self):
        self.adb = ADB()

    def inspect(self) -> DisplayInfo:

        info = DisplayInfo()

        # -----------------------------
        # Resolution
        # -----------------------------

        result = self.adb.shell(
            "wm size"
        ).stdout.strip()

        if ":" in result:

            info.resolution = result.split(":")[1].strip()

            if "x" in info.resolution:

                w, h = info.resolution.split("x")

                info.width = int(w)
                info.height = int(h)

        # -----------------------------
        # Density
        # -----------------------------

        density = self.adb.shell(
            "wm density"
        ).stdout.strip()

        if ":" in density:

            info.density = density.split(":")[1].strip()

        # -----------------------------
        # Refresh Rate
        # -----------------------------

        display = self.adb.shell(
            "dumpsys display"
        ).stdout

        for line in display.splitlines():

            if "mRefreshRate=" in line:

                try:

                    rate = line.split("mRefreshRate=")[1]

                    rate = rate.split(",")[0]

                    info.refresh_rate = float(rate)

                    break

                except Exception:
                    pass

        # -----------------------------
        # Orientation
        # -----------------------------

        if info.width > info.height:
            info.orientation = "Landscape"
        else:
            info.orientation = "Portrait"

        # -----------------------------
        # Brightness Mode
        # -----------------------------

        brightness = self.adb.shell(
            "settings get system screen_brightness_mode"
        ).stdout.strip()

        if brightness == "1":
            info.brightness_mode = "Auto"

        elif brightness == "0":
            info.brightness_mode = "Manual"

        # -----------------------------
        # HDR
        # -----------------------------

        features = self.adb.shell(
            "pm list features"
        ).stdout.lower()

        info.hdr_supported = (
            "hdr" in features
        )

        # -----------------------------
        # Screen State
        # -----------------------------

        power = self.adb.shell(
            "dumpsys power"
        ).stdout

        info.screen_on = (
            "Display Power: state=ON" in power
            or
            "mWakefulness=Awake" in power
        )

        # -----------------------------
        # Diagonal Size
        # -----------------------------

        try:
            dpi_match = re.search(r"(\d+)", info.density)
            if dpi_match and info.width and info.height:
                dpi = float(dpi_match.group(1))
                if dpi > 0:
                    diag_px = math.sqrt(info.width ** 2 + info.height ** 2)
                    info.diagonal_inches = round(diag_px / dpi, 1)
        except Exception:
            pass

        # -----------------------------
        # Color Space
        # -----------------------------

        try:
            sf = self.adb.shell("dumpsys SurfaceFlinger").stdout
            for line in sf.splitlines():
                line_lower = line.lower()
                if "display p3" in line_lower:
                    info.color_space = "Display P3"
                    break
                if "wide gamut" in line_lower or "wide_gamut" in line_lower:
                    info.color_space = "Wide Gamut"
                    break
                if "srgb" in line_lower and (
                    "colormode" in line_lower or "color space" in line_lower
                ):
                    info.color_space = "sRGB"
                    break
        except Exception:
            pass

        # -----------------------------
        # OLED Heuristic
        # -----------------------------

        try:
            model = self.adb.getprop("ro.product.model")
            if "Pixel" in model:
                m = re.search(r"Pixel\s+(\d+)", model)
                if m and int(m.group(1)) >= 6:
                    info.oled_verified = True
        except Exception:
            pass

        return info