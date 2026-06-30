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
    kernelsu_installed: bool = False
    apatch_installed: bool = False
    twrp_detected: bool = False
    orangefox_detected: bool = False
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
        # KernelSU
        # -------------------------------------------------

        if "me.weishu.kernelsu" in packages:
            info.kernelsu_installed = True
        else:
            ksu_ls = self.adb.shell("ls /data/adb/ksu").stdout.strip()
            if ksu_ls:
                info.kernelsu_installed = True

        # -------------------------------------------------
        # APatch
        # -------------------------------------------------

        if "me.bmax.apatch" in packages:
            info.apatch_installed = True
        else:
            ap_ls = self.adb.shell("ls /data/adb/ap").stdout.strip()
            if ap_ls:
                info.apatch_installed = True

        # -------------------------------------------------
        # TWRP
        # -------------------------------------------------

        twrp_prop = self.adb.getprop("ro.twrp.boot")
        if twrp_prop == "1":
            info.twrp_detected = True
        else:
            bootmode = self.adb.shell("getprop ro.bootmode").stdout.strip().lower()
            if "recovery" in bootmode:
                sbin = self.adb.shell("ls /sbin/recovery").stdout.strip()
                if sbin:
                    info.twrp_detected = True

        # -------------------------------------------------
        # OrangeFox
        # -------------------------------------------------

        if "org.orangefox" in packages:
            info.orangefox_detected = True
        else:
            ofox_prop = self.adb.getprop("ro.build.description").lower()
            if "orangefox" in ofox_prop:
                info.orangefox_detected = True

        # -------------------------------------------------
        # BusyBox
        # -------------------------------------------------

        busybox = self.adb.shell(
            "which busybox"
        ).stdout.strip()

        if busybox:
            info.busybox_installed = True

        return info