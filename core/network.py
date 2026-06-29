"""
Pixel Inspector Pro
core/network.py

Network inspection module.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.adb import ADB


@dataclass
class NetworkInfo:
    wifi_enabled: bool = False
    bluetooth_enabled: bool = False
    airplane_mode: bool = False

    mobile_data_enabled: bool = False

    carrier: str = ""
    network_type: str = ""

    sim_state: str = ""
    sim_operator: str = ""

    device_ip: str = ""

    usb_debugging: bool = False

    hostname: str = ""

    nfc_supported: bool = False


class NetworkInspector:

    def __init__(self):

        self.adb = ADB()

    def inspect(self) -> NetworkInfo:

        info = NetworkInfo()

        # -------------------------------------------------
        # WiFi
        # -------------------------------------------------

        wifi = self.adb.shell(
            "settings get global wifi_on"
        ).stdout.strip()

        info.wifi_enabled = wifi == "1"

        # -------------------------------------------------
        # Bluetooth
        # -------------------------------------------------

        bt = self.adb.shell(
            "settings get global bluetooth_on"
        ).stdout.strip()

        info.bluetooth_enabled = bt == "1"

        # -------------------------------------------------
        # Airplane Mode
        # -------------------------------------------------

        airplane = self.adb.shell(
            "settings get global airplane_mode_on"
        ).stdout.strip()

        info.airplane_mode = airplane == "1"

        # -------------------------------------------------
        # Mobile Data
        # -------------------------------------------------

        mobile = self.adb.shell(
            "settings get global mobile_data"
        ).stdout.strip()

        info.mobile_data_enabled = mobile == "1"

        # -------------------------------------------------
        # Carrier
        # -------------------------------------------------

        info.carrier = self.adb.getprop(
            "gsm.operator.alpha"
        )

        info.sim_operator = self.adb.getprop(
            "gsm.operator.numeric"
        )

        info.network_type = self.adb.getprop(
            "gsm.network.type"
        )

        info.sim_state = self.adb.getprop(
            "gsm.sim.state"
        )

        # -------------------------------------------------
        # Hostname
        # -------------------------------------------------

        info.hostname = self.adb.shell(
            "getprop net.hostname"
        ).stdout.strip()

        # -------------------------------------------------
        # IP Address
        # -------------------------------------------------

        ip = self.adb.shell(
            "ip addr show wlan0"
        ).stdout

        for line in ip.splitlines():

            line = line.strip()

            if line.startswith("inet "):

                info.device_ip = line.split()[1].split("/")[0]

                break

        # -------------------------------------------------
        # USB Debugging
        # -------------------------------------------------

        adb = self.adb.shell(
            "settings get global adb_enabled"
        ).stdout.strip()

        info.usb_debugging = adb == "1"

        # -------------------------------------------------
        # NFC
        # -------------------------------------------------

        features = self.adb.shell(
            "pm list features"
        ).stdout.lower()

        info.nfc_supported = "android.hardware.nfc" in features

        return info