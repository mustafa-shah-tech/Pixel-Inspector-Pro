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

    governor: str = ""
    gpu_model: str = ""
    gpu_frequency_mhz: int = 0

    swap_total_gb: float = 0.0
    swap_free_gb: float = 0.0

    thermal_status: str = "Unknown"


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

        swap_total = 0
        swap_free = 0

        for line in mem.splitlines():

            if line.startswith("MemTotal"):

                total = int(line.split()[1])

            elif line.startswith("MemAvailable"):

                available = int(line.split()[1])

            elif line.startswith("SwapTotal"):

                swap_total = int(line.split()[1])

            elif line.startswith("SwapFree"):

                swap_free = int(line.split()[1])

        if total:
            info.total_ram_gb = self.kb_to_gb(total)

        if available:
            info.available_ram_gb = self.kb_to_gb(available)

        if swap_total:
            info.swap_total_gb = self.kb_to_gb(swap_total)

        if swap_free:
            info.swap_free_gb = self.kb_to_gb(swap_free)

        # -------------------------------------------------
        # CPU Governor
        # -------------------------------------------------

        info.governor = self.adb.shell(
            "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
        ).stdout.strip()

        # -------------------------------------------------
        # GPU
        # -------------------------------------------------

        gpu_egl = self.adb.getprop("ro.hardware.egl")
        if gpu_egl:
            info.gpu_model = gpu_egl
        else:
            info.gpu_model = self.adb.getprop("ro.board.platform")

        gpuclk = self.adb.shell(
            "cat /sys/class/kgsl/kgsl-3d0/gpuclk"
        ).stdout.strip()

        if gpuclk.isdigit():
            info.gpu_frequency_mhz = round(int(gpuclk) / 1_000_000)

        # -------------------------------------------------
        # Thermal Status
        # -------------------------------------------------

        THERMAL_MAP = {
            "0": "Normal",
            "1": "Light",
            "2": "Moderate",
            "3": "Severe",
        }

        try:
            thermal = self.adb.shell("dumpsys thermalservice").stdout
            for line in thermal.splitlines():
                if "mStatus=" in line:
                    val = line.split("mStatus=")[1].split()[0].strip()
                    info.thermal_status = THERMAL_MAP.get(val, "Unknown")
                    break
        except Exception:
            pass

        return info