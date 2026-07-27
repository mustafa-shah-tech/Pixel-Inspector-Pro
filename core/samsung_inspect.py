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
    "com.android.chrome",
    "com.microsoft.",
    "com.facebook.",
    "com.netflix.",
    "com.spotify.",
    "com.linkedin.",
    "com.booking.",
)


# ---------------------------------------------------------------------------
# SoC codename → marketing name lookup tables
# ---------------------------------------------------------------------------

_QUALCOMM_CODENAMES = {
    "atoll":     "Snapdragon 720G/750G",
    "lahaina":   "Snapdragon 888",
    "shima":     "Snapdragon 778G",
    "yupik":     "Snapdragon 778G",
    "taro":      "Snapdragon 8 Gen 1",
    "kalama":    "Snapdragon 8 Gen 3",
    "pineapple": "Snapdragon 8 Gen 3",
    "crow":      "Snapdragon 8s Gen 3",
    "sun":       "Snapdragon 8 Elite",
    "cliffs":    "Snapdragon 8s Gen 3",
    "parrot":    "Snapdragon 4 Gen 1",
    "holi":      "Snapdragon 695",
    "bengal":    "Snapdragon 662",
    "trinket":   "Snapdragon 665",
}

_EXYNOS_CODENAMES = {
    "exynos2100": "Exynos 2100",
    "exynos2200": "Exynos 2200",
    "exynos1080": "Exynos 1080",
    "exynos1280": "Exynos 1280",
    "exynos1380": "Exynos 1380",
    "s5e9945":    "Exynos 2400",
    "s5e8835":    "Exynos 1380",
}


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
        try:
            v = int(result.one_ui_version)
            major = v // 10000
            minor = (v % 10000) // 100
            patch = v % 100
            result.one_ui_version = (
                f"{major}.{minor}.{patch}" if patch else f"{major}.{minor}"
            )
        except (ValueError, TypeError):
            pass  # leave raw string if parsing fails

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

        # Codename → marketing name lookup (applied after raw family set)
        marketing_name = _QUALCOMM_CODENAMES.get(p) or _EXYNOS_CODENAMES.get(p)
        if marketing_name:
            result.soc_family = marketing_name

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

        pkg_output = self.adb.shell("pm list packages -s").stdout
        bloat = 0

        for line in pkg_output.splitlines():
            pkg = line.replace("package:", "").strip()
            if any(pkg.startswith(prefix) for prefix in _SAMSUNG_BLOAT_PREFIXES):
                bloat += 1

        result.bloatware_count = bloat

        # ---- Finalise score -----------------------------------------------

        result.authenticity_score = max(0, min(score, 100))

        return result
