"""
Pixel Inspector Pro
core/software.py

Software inspection module.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.adb import ADB


@dataclass
class SoftwareInfo:
    installed_apps_count: int = 0
    system_apps_count: int = 0
    disabled_apps_count: int = 0
    play_services_version: str = "Unknown"
    play_protect_enabled: bool = False
    # No reliable way to check pending OTA update status via standard ADB
    # without root — the UpdateEngine / RecoverySystem APIs require privileged
    # access not exposed through unprivileged shell commands.
    update_status: str = "Unknown"


class SoftwareInspector:

    def __init__(self):
        self.adb = ADB()

    def _count_lines(self, command: str) -> int:
        output = self.adb.shell(command).stdout
        return len([l for l in output.splitlines() if l.strip()])

    def inspect(self) -> SoftwareInfo:

        info = SoftwareInfo()

        # -------------------------------------------------
        # App Counts
        # -------------------------------------------------

        # Third-party / user-installed apps (meaningful "installed apps" count)
        info.installed_apps_count = self._count_lines("pm list packages -3")

        # System apps
        info.system_apps_count = self._count_lines("pm list packages -s")

        # Disabled apps
        info.disabled_apps_count = self._count_lines("pm list packages -d")

        # -------------------------------------------------
        # Play Services Version
        # -------------------------------------------------

        try:
            dump = self.adb.shell(
                "dumpsys package com.google.android.gms"
            ).stdout

            for line in dump.splitlines():
                if "versionName=" in line:
                    info.play_services_version = (
                        line.split("versionName=", 1)[1].strip()
                    )
                    break

        except Exception:
            pass

        # -------------------------------------------------
        # Play Protect
        # -------------------------------------------------

        verifier = self.adb.shell(
            "settings get global package_verifier_enable"
        ).stdout.strip()

        info.play_protect_enabled = (verifier == "1")

        return info
