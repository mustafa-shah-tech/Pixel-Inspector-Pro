"""
Pixel Inspector Pro
core/camera.py

Camera inspection module.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.adb import ADB


@dataclass
class CameraInfo:
    camera_count: int = 0

    has_front_camera: bool = False
    has_back_camera: bool = False

    has_flash: bool = False
    has_autofocus: bool = False

    camera2_api: bool = False

    logical_multi_camera: bool = False

    external_camera: bool = False

    camera_ids: list[str] = field(default_factory=list)


class CameraInspector:

    def __init__(self):

        self.adb = ADB()

    def inspect(self) -> CameraInfo:

        info = CameraInfo()

        # -------------------------------------------------
        # Camera Features
        # -------------------------------------------------

        feature_lines = [
            l.strip()
            for l in self.adb.shell("pm list features").stdout.lower().splitlines()
        ]

        info.has_front_camera = (
            "feature:android.hardware.camera.front" in feature_lines
        )

        info.has_back_camera = (
            "feature:android.hardware.camera" in feature_lines
        )

        info.has_flash = (
            "feature:android.hardware.camera.flash" in feature_lines
        )

        info.has_autofocus = (
            "feature:android.hardware.camera.autofocus" in feature_lines
        )

        info.camera2_api = (
            "feature:android.hardware.camera.level.full" in feature_lines
            or
            "feature:android.hardware.camera.capability.manual_post_processing"
            in feature_lines
        )

        info.logical_multi_camera = (
            "feature:android.hardware.camera.logical_multi_camera" in feature_lines
        )

        info.external_camera = (
            "feature:android.hardware.camera.external" in feature_lines
        )

        # -------------------------------------------------
        # Camera IDs
        # -------------------------------------------------

        dump = self.adb.shell(
            "dumpsys media.camera"
        ).stdout

        ids = []

        for line in dump.splitlines():

            line = line.strip()

            if line.startswith("Camera ID"):

                try:
                    cid = line.split(":")[1].strip()

                    ids.append(cid)

                except Exception:
                    pass

        info.camera_ids = sorted(list(set(ids)))

        info.camera_count = len(info.camera_ids)

        # -------------------------------------------------
        # Fallback if dumpsys didn't expose IDs
        # -------------------------------------------------

        if info.camera_count == 0:

            if info.has_front_camera:
                info.camera_count += 1

            if info.has_back_camera:
                info.camera_count += 1

        return info