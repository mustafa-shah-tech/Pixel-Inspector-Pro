"""
Android Inspector Pro
core/generic_inspect.py

Generic Android inspection module — fallback for any brand that is
neither Google Pixel nor Samsung. Runs the universal integrity checks
that are meaningful on any AOSP-derived firmware.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.adb import ADB


@dataclass
class GenericInspectionResult:

    manufacturer: str = ""
    model: str = ""
    build_fingerprint: str = ""

    # Boot integrity
    bootloader_locked: bool = False
    verified_boot: str = ""        # green | orange | yellow | red

    # Build authenticity
    official_build: bool = False   # fingerprint contains no "test-keys"
    build_tags: str = ""

    # GSI / custom ROM heuristic
    gsi_suspected: bool = False
    brand: str = ""
    system_brand: str = ""

    # Overall
    authenticity_score: int = 0
    issues: list[str] = field(default_factory=list)


class GenericInspector:

    def __init__(self):
        self.adb = ADB()

    def inspect(self) -> GenericInspectionResult:

        result = GenericInspectionResult()
        score = 100

        # ---- Basic identity -----------------------------------------------

        result.manufacturer = self.adb.getprop("ro.product.manufacturer")
        result.model = self.adb.getprop("ro.product.model")
        result.build_fingerprint = self.adb.getprop("ro.build.fingerprint")

        # ---- Bootloader ---------------------------------------------------

        locked = self.adb.getprop("ro.boot.flash.locked")

        if locked == "1":
            result.bootloader_locked = True
        elif locked == "0":
            result.bootloader_locked = False
            score -= 15
            result.issues.append("Bootloader is unlocked.")

        # ---- Verified boot ------------------------------------------------

        vb = self.adb.getprop("ro.boot.verifiedbootstate")
        result.verified_boot = vb

        if vb.lower() == "red":
            score -= 20
            result.issues.append("Verified Boot is RED.")
        elif vb.lower() == "orange":
            score -= 10
            result.issues.append("Verified Boot is ORANGE (bootloader unlocked).")

        # ---- Build tags ---------------------------------------------------

        build_tags = self.adb.getprop("ro.build.tags")
        result.build_tags = build_tags

        if build_tags.strip() == "test-keys":
            result.official_build = False
            score -= 25
            result.issues.append(
                "Build tags indicate test-keys — not an official release build."
            )
        else:
            result.official_build = True

        # ---- GSI heuristic ------------------------------------------------

        brand = self.adb.getprop("ro.product.brand")
        system_brand = self.adb.getprop("ro.product.system.brand")

        result.brand = brand
        result.system_brand = system_brand

        if (
            brand
            and system_brand
            and brand.lower() != system_brand.lower()
        ):
            result.gsi_suspected = True
            score -= 20
            result.issues.append(
                "Possible GSI ROM detected (system brand mismatch)."
            )

        # ---- Finalise -----------------------------------------------------

        result.authenticity_score = max(0, min(score, 100))

        return result
