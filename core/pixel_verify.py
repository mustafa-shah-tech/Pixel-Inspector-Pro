"""
Pixel Inspector Pro
core/pixel_verify.py
"""

from __future__ import annotations

from dataclasses import dataclass

from core.device import DeviceInspector
from core.security import SecurityInspector


@dataclass
class PixelVerificationResult:
    genuine_pixel: bool = False

    model: str = ""
    codename: str = ""
    manufacturer: str = ""
    fingerprint: str = ""

    expected_codename: str = ""
    codename_match: bool = False

    tensor_chip: str = "Unknown"

    official_build: bool = False
    bootloader_locked: bool = False
    verified_boot: str = "Unknown"

    authenticity_score: int = 0

    issues: list[str] | None = None


PIXEL_DATABASE = {

    "Pixel 6": {
        "codename": "oriole",
        "tensor": "Tensor G1",
    },

    "Pixel 6 Pro": {
        "codename": "raven",
        "tensor": "Tensor G1",
    },

    "Pixel 6a": {
        "codename": "bluejay",
        "tensor": "Tensor G1",
    },

    "Pixel 7": {
        "codename": "panther",
        "tensor": "Tensor G2",
    },

    "Pixel 7 Pro": {
        "codename": "cheetah",
        "tensor": "Tensor G2",
    },

    "Pixel 7a": {
        "codename": "lynx",
        "tensor": "Tensor G2",
    },

    "Pixel Fold": {
        "codename": "felix",
        "tensor": "Tensor G2",
    },

    "Pixel Tablet": {
        "codename": "tangorpro",
        "tensor": "Tensor G2",
    },

    "Pixel 8": {
        "codename": "shiba",
        "tensor": "Tensor G3",
    },

    "Pixel 8 Pro": {
        "codename": "husky",
        "tensor": "Tensor G3",
    },

    "Pixel 8a": {
        "codename": "akita",
        "tensor": "Tensor G3",
    },

    "Pixel 9": {
        "codename": "tokay",
        "tensor": "Tensor G4",
    },

    "Pixel 9 Pro": {
        "codename": "caiman",
        "tensor": "Tensor G4",
    },

    "Pixel 9 Pro XL": {
        "codename": "komodo",
        "tensor": "Tensor G4",
    },

    "Pixel 9 Pro Fold": {
        "codename": "comet",
        "tensor": "Tensor G4",
    },

    "Pixel 9a": {
        "codename": "tegu",
        "tensor": "Tensor G4",
    },

}


class PixelVerifier:

    def __init__(self):

        self.device = DeviceInspector()
        self.security = SecurityInspector()

    def verify(self):

        device = self.device.inspect()
        security = self.security.inspect()

        result = PixelVerificationResult()

        result.model = device.model
        result.codename = device.device
        result.manufacturer = device.manufacturer
        result.fingerprint = device.fingerprint

        result.bootloader_locked = security.bootloader_locked
        result.verified_boot = security.verified_boot

        result.issues = []

        score = 100

        # Manufacturer

        if device.manufacturer.lower() != "google":

            score -= 30
            result.issues.append(
                "Manufacturer is not Google."
            )

        else:

            result.genuine_pixel = True

        # Model

        if device.model not in PIXEL_DATABASE:

            score -= 40
            result.issues.append(
                "Unknown Pixel model."
            )

        else:

            expected = PIXEL_DATABASE[device.model]

            result.expected_codename = expected["codename"]
            result.tensor_chip = expected["tensor"]

            if device.device == expected["codename"]:

                result.codename_match = True

            else:

                score -= 20

                result.issues.append(
                    f"Codename mismatch. Expected {expected['codename']}."
                )

        # Build Fingerprint

        if "google" in device.fingerprint.lower():

            result.official_build = True

        else:

            score -= 20

            result.issues.append(
                "Non-Google build fingerprint."
            )

        # Bootloader

        if not security.bootloader_locked:

            score -= 15

            result.issues.append(
                "Bootloader unlocked."
            )

        # Verified Boot

        if security.verified_boot.lower() != "green":

            score -= 15

            result.issues.append(
                "Verified Boot is not GREEN."
            )

        if score < 0:
            score = 0

        result.authenticity_score = score

        return result