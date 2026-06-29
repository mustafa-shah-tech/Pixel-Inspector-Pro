"""
Pixel Inspector Pro
core/storage.py

Storage inspection module.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.adb import ADB


@dataclass
class StorageInfo:
    filesystem: str = ""
    total_gb: float = 0.0
    used_gb: float = 0.0
    free_gb: float = 0.0
    usage_percent: float = 0.0
    mount_point: str = "/data"


class StorageInspector:

    def __init__(self):
        self.adb = ADB()

    @staticmethod
    def _kb_to_gb(value: int) -> float:
        return round(value / (1024 * 1024), 2)

    def inspect(self) -> StorageInfo:

        info = StorageInfo()

        result = self.adb.storage()

        lines = result.strip().splitlines()

        if len(lines) < 2:
            return info

        # Expected format:
        # Filesystem 1K-blocks Used Available Use% Mounted on

        parts = lines[-1].split()

        if len(parts) < 6:
            return info

        info.filesystem = parts[0]

        total = int(parts[1])
        used = int(parts[2])
        free = int(parts[3])

        info.total_gb = self._kb_to_gb(total)
        info.used_gb = self._kb_to_gb(used)
        info.free_gb = self._kb_to_gb(free)

        info.usage_percent = round((used / total) * 100, 1)

        info.mount_point = parts[-1]

        return info