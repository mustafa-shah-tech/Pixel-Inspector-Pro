"""
Pixel Inspector Pro
core/battery.py
"""

from __future__ import annotations

from dataclasses import dataclass

from core.adb import ADB


@dataclass
class BatteryInfo:
    level: int = 0

    status: str = "Unknown"
    health: str = "Unknown"

    temperature: float = 0.0
    voltage: int = 0

    technology: str = ""

    ac_powered: bool = False
    usb_powered: bool = False
    wireless_powered: bool = False

    present: bool = False

    charge_counter: int | None = None
    charge_full: int | None = None
    charge_full_design: int | None = None
    capacity_percent: float | None = None

    cycle_count: int | None = None

    charging_type: str = "Unknown"
    usb_current_ma: int | None = None
    battery_score: int = 0


class BatteryInspector:

    HEALTH_MAP = {
        1: "Unknown",
        2: "Good",
        3: "Overheat",
        4: "Dead",
        5: "Over Voltage",
        6: "Failure",
        7: "Cold",
    }

    STATUS_MAP = {
        1: "Unknown",
        2: "Charging",
        3: "Discharging",
        4: "Not Charging",
        5: "Full",
    }

    def __init__(self):
        self.adb = ADB()

    def _read_int(self, path):

        result = self.adb.shell(f"cat {path}")

        value = result.stdout.strip()

        if value.isdigit():
            return int(value)

        return None

    def inspect(self) -> BatteryInfo:

        info = BatteryInfo()

        battery = self.adb.shell(
            "dumpsys battery"
        ).stdout

        for line in battery.splitlines():

            line = line.strip()

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip().lower()
            value = value.strip()

            if key == "level":
                info.level = int(value)

            elif key == "temperature":
                info.temperature = int(value) / 10

            elif key == "voltage":
                info.voltage = int(value)

            elif key == "technology":
                info.technology = value

            elif key == "present":
                info.present = value.lower() == "true"

            elif key == "ac powered":
                info.ac_powered = value.lower() == "true"

            elif key == "usb powered":
                info.usb_powered = value.lower() == "true"

            elif key == "wireless powered":
                info.wireless_powered = value.lower() == "true"

            elif key == "health":

                try:
                    info.health = self.HEALTH_MAP.get(
                        int(value),
                        value
                    )
                except:
                    info.health = value

            elif key == "status":

                try:
                    info.status = self.STATUS_MAP.get(
                        int(value),
                        value
                    )
                except:
                    info.status = value

        # ---------------------------------
        # Capacity
        # ---------------------------------

        info.charge_counter = self._read_int(
            "/sys/class/power_supply/battery/charge_counter"
        )

        info.charge_full = self._read_int(
            "/sys/class/power_supply/battery/charge_full"
        )

        info.charge_full_design = self._read_int(
            "/sys/class/power_supply/battery/charge_full_design"
        )

        if (
            info.charge_full
            and
            info.charge_full_design
        ):

            info.capacity_percent = round(
                info.charge_full /
                info.charge_full_design * 100,
                1
            )

        # ---------------------------------
        # Cycle Count
        # ---------------------------------

        info.cycle_count = self._read_int(
            "/sys/class/power_supply/battery/cycle_count"
        )

        # ---------------------------------
        # Charging Type
        # ---------------------------------

        if info.wireless_powered:
            info.charging_type = "Wireless"
        elif info.ac_powered:
            info.charging_type = "AC/Fast Charging"
        elif info.usb_powered:
            info.charging_type = "USB"
        else:
            info.charging_type = "Not Charging"

        # ---------------------------------
        # USB Current
        # ---------------------------------

        raw_ua = self._read_int("/sys/class/power_supply/usb/current_now")
        if raw_ua is not None:
            info.usb_current_ma = round(raw_ua / 1000)

        # ---------------------------------
        # Battery Score
        # ---------------------------------

        bscore = 100

        if info.capacity_percent is not None:
            if info.capacity_percent < 80:
                bscore -= 30
            elif info.capacity_percent < 90:
                bscore -= 15

        if info.health not in ("Good", "Unknown"):
            bscore -= 20

        if info.temperature > 45:
            bscore -= 15

        if info.cycle_count is not None and info.cycle_count > 500:
            bscore -= 10

        info.battery_score = max(0, min(bscore, 100))

        return info