"""
Pixel Inspector Pro
core/sensors.py

Sensor inspection module.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.adb import ADB


@dataclass
class SensorInfo:
    total_sensors: int = 0

    accelerometer: bool = False
    gyroscope: bool = False
    magnetometer: bool = False
    proximity: bool = False
    light: bool = False
    barometer: bool = False
    fingerprint: bool = False
    step_counter: bool = False
    step_detector: bool = False
    heart_rate: bool = False
    gps: bool = False

    sensor_list: list[str] = field(default_factory=list)


class SensorInspector:

    def __init__(self):
        self.adb = ADB()

    def inspect(self) -> SensorInfo:

        info = SensorInfo()

        dump = self.adb.shell(
            "dumpsys sensorservice"
        ).stdout

        sensors = []

        for line in dump.splitlines():

            line = line.strip()

            if "|" not in line:
                continue

            if ")" not in line:
                continue

            try:
                name = line.split(")")[1].split("|")[0].strip()

                if name:

                    sensors.append(name)

            except Exception:
                pass

        sensors = sorted(list(set(sensors)))

        info.sensor_list = sensors
        info.total_sensors = len(sensors)

        lower = " ".join(sensors).lower()

        info.accelerometer = "accelerometer" in lower
        info.gyroscope = "gyro" in lower
        info.magnetometer = (
            "magnetic" in lower or
            "magnetometer" in lower
        )
        info.proximity = "proximity" in lower
        info.light = "light" in lower
        info.barometer = (
            "pressure" in lower or
            "barometer" in lower
        )
        info.step_counter = "step counter" in lower
        info.step_detector = "step detector" in lower
        info.heart_rate = "heart" in lower
        info.gps = (
            "gps" in lower or
            "gnss" in lower
        )

        # Fingerprint: check BiometricManager / pm list features
        # (sensorservice rarely exposes fingerprint sensors directly)
        fp_features = [
            l.strip()
            for l in self.adb.shell("pm list features").stdout.lower().splitlines()
        ]
        info.fingerprint = (
            "feature:android.hardware.fingerprint" in fp_features
            or "feature:android.hardware.biometrics.fingerprint" in fp_features
        )

        return info