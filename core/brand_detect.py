"""
Android Inspector Pro
core/brand_detect.py

Brand detection layer.
Reads the already-populated Device object and returns a canonical
brand string that Inspector.inspect() uses to pick the right module.
"""

from __future__ import annotations

from core.device import Device


def detect_brand(device: Device) -> str:
    """
    Return one of: "pixel" | "samsung" | "generic"

    Decision is based solely on ro.product.manufacturer, which
    DeviceInspector already fetches before this function is called.
    No additional ADB round-trips are made here.
    """

    mfr = device.manufacturer.strip().lower()

    if mfr == "google":
        return "pixel"

    if mfr == "samsung":
        return "samsung"

    return "generic"
