"""
Pixel Inspector Pro
core/display.py

Display inspection module.
"""

from __future__ import annotations

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

        return info