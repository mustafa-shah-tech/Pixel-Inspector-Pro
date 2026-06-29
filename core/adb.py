"""
Pixel Inspector Pro
core/adb.py

ADB communication layer.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from core.utils import executable_exists


class ADBError(Exception):
    """Raised when an ADB operation fails."""


class ADB:
    """
    Wrapper around Android Debug Bridge.
    """

    def __init__(self, adb_path: Optional[str] = None):

        self.adb = adb_path or self.find_adb()

        if self.adb is None:
            raise ADBError(
                "ADB executable not found. "
                "Install Android Platform Tools or place adb.exe in PATH."
            )

    # --------------------------------------------------------

    @staticmethod
    def find_adb() -> Optional[str]:
        """
        Locate adb.exe
        """

        if executable_exists("adb"):
            return "adb"

        possible = [
            r"C:\platform-tools\adb.exe",
            r"C:\Android\platform-tools\adb.exe",
            str(Path.home() / "platform-tools" / "adb.exe"),
            str(Path.home() / "AppData/Local/Android/Sdk/platform-tools/adb.exe"),
        ]

        for path in possible:
            if Path(path).exists():
                return path

        return None

    # --------------------------------------------------------

    def command(self, *args, timeout=10):

        process = subprocess.run(
            [self.adb, *args],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return process

    # --------------------------------------------------------

    def shell(self, command: str):

        return self.command("shell", command)

    # --------------------------------------------------------

    def start_server(self):

        return self.command("start-server")

    # --------------------------------------------------------

    def kill_server(self):

        return self.command("kill-server")

    # --------------------------------------------------------

    def version(self):

        return self.command("version").stdout.strip()

    # --------------------------------------------------------

    def devices(self):

        result = self.command("devices")

        devices = []

        for line in result.stdout.splitlines()[1:]:

            if "\tdevice" in line:

                serial = line.split()[0]

                devices.append(serial)

        return devices

    # --------------------------------------------------------

    def is_connected(self):

        return len(self.devices()) > 0

    # --------------------------------------------------------

    def getprop(self, prop: str):

        return self.shell(f"getprop {prop}").stdout.strip()

    # --------------------------------------------------------

    def dumpsys(self, service: str):

        return self.shell(f"dumpsys {service}").stdout

    # --------------------------------------------------------

    def battery(self):

        return self.dumpsys("battery")

    # --------------------------------------------------------

    def cpuinfo(self):

        return self.shell("cat /proc/cpuinfo").stdout

    # --------------------------------------------------------

    def meminfo(self):

        return self.shell("cat /proc/meminfo").stdout

    # --------------------------------------------------------

    def storage(self):

        return self.shell("df /data").stdout

    # --------------------------------------------------------

    def reboot(self):

        return self.command("reboot")

    # --------------------------------------------------------

    def serial(self):

        return self.getprop("ro.serialno")

    # --------------------------------------------------------

    def model(self):

        return self.getprop("ro.product.model")

    # --------------------------------------------------------

    def manufacturer(self):

        return self.getprop("ro.product.manufacturer")

    # --------------------------------------------------------

    def android_version(self):

        return self.getprop("ro.build.version.release")

    # --------------------------------------------------------

    def sdk(self):

        return self.getprop("ro.build.version.sdk")

    # --------------------------------------------------------

    def fingerprint(self):

        return self.getprop("ro.build.fingerprint")

    # --------------------------------------------------------

    def security_patch(self):

        return self.getprop("ro.build.version.security_patch")