"""
Pixel Inspector Pro
core/security.py

Security inspection module.
"""

from __future__ import annotations

from dataclasses import dataclass

from core.adb import ADB


@dataclass
class SecurityInfo:
    bootloader_locked: bool | None = None
    verified_boot: str = "Unknown"

    rooted: bool = False
    magisk_installed: bool = False
    busybox_installed: bool = False

    oem_unlock_supported: bool = False

    security_patch: str = ""

    build_type: str = ""

    encryption: str = ""


class SecurityInspector:

    def __init__(self):

        self.adb = ADB()

    def inspect(self) -> SecurityInfo:

        info = SecurityInfo()

        # -------------------------------------------------
        # Bootloader
        # -------------------------------------------------

        locked = self.adb.getprop("ro.boot.flash.locked")

        if locked == "1":
            info.bootloader_locked = True

        elif locked == "0":
            info.bootloader_locked = False

        # -------------------------------------------------
        # Verified Boot
        # -------------------------------------------------

        info.verified_boot = self.adb.getprop(
            "ro.boot.verifiedbootstate"
        )

        # -------------------------------------------------
        # Security Patch
        # -------------------------------------------------

        info.security_patch = self.adb.getprop(
            "ro.build.version.security_patch"
        )

        # -------------------------------------------------
        # Build Type
        # -------------------------------------------------

        info.build_type = self.adb.getprop(
            "ro.build.type"
        )

        # -------------------------------------------------
        # Encryption
        # -------------------------------------------------

        info.encryption = self.adb.getprop(
            "ro.crypto.state"
        )

        # -------------------------------------------------
        # OEM Unlock
        # -------------------------------------------------

        oem = self.adb.getprop(
            "ro.oem_unlock_supported"
        )

        info.oem_unlock_supported = oem == "1"

        # -------------------------------------------------
        # Root Detection
        # -------------------------------------------------

        root = self.adb.shell("which su").stdout.strip()

        if root:
            info.rooted = True

        # -------------------------------------------------
        # Magisk
        # -------------------------------------------------

        packages = self.adb.shell(
            "pm list packages"
        ).stdout.lower()

        if "magisk" in packages:
            info.magisk_installed = True

        # -------------------------------------------------
        # BusyBox
        # -------------------------------------------------

        busybox = self.adb.shell(
            "which busybox"
        ).stdout.strip()

        if busybox:
            info.busybox_installed = True

        return info