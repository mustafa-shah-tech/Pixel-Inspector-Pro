"""
Pixel Inspector Pro
core/device.py

Device model and device information collector.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from core.adb import ADB


@dataclass
class Device:
    """
    Represents a connected Android device.
    """

    serial: str = ""
    manufacturer: str = ""
    model: str = ""
    codename: str = ""
    android_version: str = ""
    sdk: str = ""
    build_fingerprint: str = ""
    security_patch: str = ""

    cpu: str = ""
    ram: str = ""
    storage: str = ""

    battery_level: int = -1

    bootloader_locked: Optional[bool] = None
    verified_boot: str = ""

    score: int = 0


class DeviceInspector:
    """
    Collects information from the connected device.
    """

    def __init__(self):
        self.adb = ADB()

    def is_connected(self) -> bool:
        return self.adb.is_connected()

    def get_device(self) -> Device:

        device = Device()

        device.serial = self.adb.serial()
        device.manufacturer = self.adb.manufacturer()
        device.model = self.adb.model()

        device.codename = self.adb.getprop("ro.product.device")

        device.android_version = self.adb.android_version()
        device.sdk = self.adb.sdk()

        device.build_fingerprint = self.adb.fingerprint()

        device.security_patch = self.adb.security_patch()

        # -------- Battery --------

        battery = self.adb.battery()

        for line in battery.splitlines():

            line = line.strip()

            if line.startswith("level:"):

                try:
                    device.battery_level = int(line.split(":")[1].strip())
                except ValueError:
                    pass

        # -------- CPU --------

        cpu = self.adb.cpuinfo()

        if cpu:
            first_line = cpu.splitlines()[0]
            device.cpu = first_line

        # -------- RAM --------

        mem = self.adb.meminfo()

        for line in mem.splitlines():

            if line.startswith("MemTotal"):

                device.ram = line.split(":")[1].strip()

                break

        # -------- Storage --------

        storage = self.adb.storage()

        if storage:
            lines = storage.splitlines()

            if len(lines) >= 2:
                device.storage = lines[-1]

        # -------- Bootloader --------

        locked = self.adb.getprop("ro.boot.flash.locked")

        if locked == "1":
            device.bootloader_locked = True
        elif locked == "0":
            device.bootloader_locked = False

        # -------- Verified Boot --------

        device.verified_boot = self.adb.getprop(
            "ro.boot.verifiedbootstate"
        )

        return device