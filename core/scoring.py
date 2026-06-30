"""
Pixel Inspector Pro
core/scoring.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScoreResult:
    total_score: int
    grade: str
    recommendation: str
    deductions: list[str]


class ScoringEngine:

    def calculate(
        self,
        battery,
        security,
        storage,
        display,
        cpu,
        camera,
        sensors,
        network,
    ) -> ScoreResult:

        score = 100
        deductions = []

        # -----------------------------
        # Battery (30 points)
        # -----------------------------

        if battery.level < 20:
            score -= 10
            deductions.append("Battery charge is very low.")

        if battery.temperature > 45:
            score -= 10
            deductions.append("Battery temperature is high.")

        if hasattr(battery, "capacity_percent"):
            if battery.capacity_percent is not None:
                if battery.capacity_percent < 80:
                    score -= 15
                    deductions.append("Battery health below 80%.")

                elif battery.capacity_percent < 90:
                    score -= 8
                    deductions.append("Battery health slightly degraded.")

        # -----------------------------
        # Security (25 points)
        # -----------------------------

        if security.rooted:
            score -= 25
            deductions.append("Device is rooted.")

        if security.magisk_installed:
            score -= 20
            deductions.append("Magisk detected.")

        if security.kernelsu_installed:
            score -= 20
            deductions.append("KernelSU detected.")

        if security.apatch_installed:
            score -= 20
            deductions.append("APatch detected.")

        if security.twrp_detected:
            score -= 20
            deductions.append("TWRP recovery detected.")

        if security.orangefox_detected:
            score -= 20
            deductions.append("OrangeFox recovery detected.")

        if security.bootloader_locked is False:
            score -= 15
            deductions.append("Bootloader unlocked.")

        if security.verified_boot.lower() == "red":
            score -= 20
            deductions.append("Verified Boot RED.")


        # -----------------------------
        # Storage
        # -----------------------------

        if storage.free_gb < 5:
            score -= 5
            deductions.append("Very little free storage.")

        # -----------------------------
        # Display
        # -----------------------------

        if display.refresh_rate < 90:
            score -= 3
            deductions.append("Refresh rate below 90Hz.")

        # -----------------------------
        # Camera
        # -----------------------------

        if not camera.has_front_camera:
            score -= 10
            deductions.append("Front camera missing.")

        if not camera.has_back_camera:
            score -= 25
            deductions.append("Rear camera missing.")

        if not camera.has_flash:
            score -= 5
            deductions.append("Flash not detected.")

        # -----------------------------
        # Sensors
        # -----------------------------

        if not sensors.fingerprint:
            score -= 8
            deductions.append("Fingerprint sensor missing.")

        if not sensors.gyroscope:
            score -= 5
            deductions.append("Gyroscope missing.")

        if not sensors.accelerometer:
            score -= 5
            deductions.append("Accelerometer missing.")

        # -----------------------------
        # Network
        # -----------------------------

        if network.airplane_mode:
            deductions.append("Airplane mode enabled.")

        # -----------------------------

        score = max(0, min(score, 100))

        if score >= 95:
            grade = "A+"
            recommendation = "Excellent Buy"

        elif score >= 90:
            grade = "A"
            recommendation = "Highly Recommended"

        elif score >= 80:
            grade = "B"
            recommendation = "Good Buy"

        elif score >= 70:
            grade = "C"
            recommendation = "Acceptable"

        elif score >= 60:
            grade = "D"
            recommendation = "Buy Only If Cheap"

        else:
            grade = "F"
            recommendation = "Avoid"

        return ScoreResult(
            total_score=score,
            grade=grade,
            recommendation=recommendation,
            deductions=deductions,
        )
        