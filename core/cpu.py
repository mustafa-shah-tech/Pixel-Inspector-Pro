"""
Pixel Inspector Pro
core/cpu.py

CPU & Memory inspection module.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.adb import ADB


@dataclass
class CpuInfo:
    hardware: str = ""
    processor: str = ""
    architecture: str = ""

    cores: int = 0

    max_frequency_mhz: int = 0
    min_frequency_mhz: int = 0

    total_ram_gb: float = 0.0
    available_ram_gb: float = 0.0

    abi: str = ""
    abi2: str = ""


class CpuInspector:

    def __init__(self):

        self.adb = ADB()

    @staticmethod
    def kb_to_gb(value: int):

        return round(value / 1024 / 1024, 2)

    def inspect(self) -> CpuInfo:

        info = CpuInfo()

        # -------------------------------------------------
        # Hardware
        # -------------------------------------------------

        info.hardware = self.adb.getprop(
            "ro.hardware"
        )

        info.processor = self.adb.getprop(
            "ro.soc.model"
        )

        info.architecture = self.adb.shell(
            "uname -m"
        ).stdout.strip()

        info.abi = self.adb.getprop(
            "ro.product.cpu.abi"
        )

        info.abi2 = self.adb.getprop(
            "ro.product.cpu.abilist"
        )

        # -------------------------------------------------
        # CPU Cores
        # -------------------------------------------------

        cpuinfo = self.adb.shell(
            "cat /proc/cpuinfo"
        ).stdout

        info.cores = cpuinfo.count("processor")

        # -------------------------------------------------
        # CPU Frequency
        # -------------------------------------------------

        max_freq = self.adb.shell(
            "cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"
        ).stdout.strip()

        min_freq = self.adb.shell(
            "cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq"
        ).stdout.strip()

        if max_freq.isdigit():
            info.max_frequency_mhz = int(max_freq) // 1000

        if min_freq.isdigit():
            info.min_frequency_mhz = int(min_freq) // 1000

        # -------------------------------------------------
        # Memory
        # -------------------------------------------------

        mem = self.adb.shell(
            "cat /proc/meminfo"
        ).stdout

        total = 0
        available = 0

        for line in mem.splitlines():

            if line.startswith("MemTotal"):

                total = int(line.split()[1])

            elif line.startswith("MemAvailable"):

                available = int(line.split()[1])

        if total:
            info.total_ram_gb = self.kb_to_gb(total)

        if available:
            info.available_ram_gb = self.kb_to_gb(available)

        return info