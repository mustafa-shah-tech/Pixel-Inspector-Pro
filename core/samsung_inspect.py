"""
Android Inspector Pro
core/samsung_inspect.py

Samsung-specific inspection module.
Runs after the shared modules have already collected the Device object.
All Samsung-unique data is gathered here via targeted ADB getprop calls
and package-manager queries.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.adb import ADB


# ---------------------------------------------------------------------------
# Known Samsung bloatware package prefixes
# ---------------------------------------------------------------------------

_SAMSUNG_BLOAT_PREFIXES = (
    "com.samsung.",
    "com.sec.",
    "com.knox.",
    "com.svox.",
    "com.skms.",
    "com.dsi.ant.",
    "com.wssnps.",
    "com.samsungapps.",
    "com.slsi.",
)


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class SamsungInspectionResult:

    # One UI
    one_ui_version: str = ""

    # SoC
    board_platform: str = ""
    soc_family: str = ""           # "Exynos" | "Snapdragon" | "Unknown"

    # Knox
    warranty_bit: str = ""         # "0" = intact, "1" = permanently void
    warranty_voided: bool = False
    flash_locked: str = ""         # ro.boot.flash.locked raw value
    knox_guard: str = ""           # ro.boot.knoxguard if present

    # Boot integrity
    dm_verity_mode: str = ""       # enforcing | disabled | ...
    verified_boot: str = ""

    # DeX
    dex_supported: bool = False

    # Build authenticity
    official_samsung_build: bool = False
    build_fingerprint: str = ""

    # Bloatware
    bloatware_count: int = 0

    # Overall
    authenticity_score: int = 0
    issues: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Inspector class
# ---------------------------------------------------------------------------

class SamsungInspector:

    def __init__(self):
        self.adb = ADB()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def inspect(self) -> SamsungInspectionResult:

        result = SamsungInspectionResult()
        score = 100

        # ---- One UI -------------------------------------------------------

        result.one_ui_version = self.adb.getprop("ro.build.version.oneui")

        # ---- SoC family ---------------------------------------------------

        platform = self.adb.getprop("ro.board.platform")
        result.board_platform = platform

        p = platform.lower()
        if p.startswith("exynos") or p.startswith("s5e") or p.startswith("universal"):
            result.soc_family = "Exynos"
        elif p.startswith("sm-") or p.startswith("sm_") or p.startswith("snapdragon") or p.startswith("kona") or p.startswith("lahaina") or p.startswith("taro") or p.startswith("kalama"):
            result.soc_family = "Snapdragon"
        elif p:
            result.soc_family = platform  # return raw if unrecognised
        else:
            result.soc_family = "Unknown"

        # ---- Knox warranty bit --------------------------------------------

        warranty_bit = self.adb.getprop("ro.boot.warranty_bit")
        result.warranty_bit = warranty_bit

        if warranty_bit == "1":
            result.warranty_voided = True
            score -= 40
            result.issues.append(
                "Knox warranty bit is 1 — warranty permanently voided."
            )

        # ---- Flash locked cross-check -------------------------------------

        flash_locked = self.adb.getprop("ro.boot.flash.locked")
        result.flash_locked = flash_locked

        if flash_locked == "0" and warranty_bit != "1":
            # Bootloader unlocked but warranty counter not yet tripped
            score -= 20
            result.issues.append(
                "Bootloader is unlocked (flash.locked = 0)."
            )
        elif flash_locked == "0" and warranty_bit == "1":
            # Already captured above; no double-deduction
            pass

        # ---- KnoxGuard ----------------------------------------------------

        kg = self.adb.getprop("ro.boot.knoxguard")
        result.knox_guard = kg

        if kg and kg.lower() not in ("", "none", "0", "inactive", "unknown"):
            score -= 15
            result.issues.append(
                f"KnoxGuard is active: {kg}."
            )

        # ---- dm-verity status ---------------------------------------------

        cmdline = self.adb.shell("cat /proc/cmdline").stdout
        dm_verity = "unknown"

        for token in cmdline.split():
            if token.startswith("androidboot.veritymode="):
                dm_verity = token.split("=", 1)[1]
                break

        result.dm_verity_mode = dm_verity

        if dm_verity.lower() == "disabled":
            score -= 20
            result.issues.append(
                "dm-verity is disabled — system partition may have been modified."
            )

        # ---- Verified boot ------------------------------------------------

        vb = self.adb.getprop("ro.boot.verifiedbootstate")
        result.verified_boot = vb

        if vb.lower() == "red":
            score -= 20
            result.issues.append("Verified Boot is RED.")
        elif vb.lower() == "orange":
            score -= 10
            result.issues.append("Verified Boot is ORANGE (bootloader unlocked).")

        # ---- DeX support --------------------------------------------------

        characteristics = self.adb.getprop("ro.build.characteristics")
        result.dex_supported = "desktop" in characteristics.lower()

        # ---- Official Samsung build ---------------------------------------

        fingerprint = self.adb.getprop("ro.build.fingerprint")
        result.build_fingerprint = fingerprint
        manufacturer = self.adb.getprop("ro.product.manufacturer")

        if (
            "samsung" in fingerprint.lower()
            and manufacturer.lower() == "samsung"
        ):
            result.official_samsung_build = True
        else:
            score -= 25
            result.issues.append(
                "Build fingerprint does not match Samsung official build."
            )

        # ---- Samsung bloatware count --------------------------------------

        pkg_output = self.adb.shell("pm list packages").stdout
        bloat = 0

        for line in pkg_output.splitlines():
            pkg = line.replace("package:", "").strip()
            if any(pkg.startswith(prefix) for prefix in _SAMSUNG_BLOAT_PREFIXES):
                bloat += 1

        result.bloatware_count = bloat

        # ---- Finalise score -----------------------------------------------

        result.authenticity_score = max(0, min(score, 100))

        return result
