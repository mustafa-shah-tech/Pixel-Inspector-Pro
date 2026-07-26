"""
Android Inspector Pro
core/inspector.py
"""

from __future__ import annotations

from dataclasses import dataclass

from core.device import DeviceInspector
from core.battery import BatteryInspector
from core.display import DisplayInspector
from core.camera import CameraInspector
from core.cpu import CpuInspector
from core.storage import StorageInspector
from core.network import NetworkInspector
from core.security import SecurityInspector
from core.sensors import SensorInspector
from core.software import SoftwareInspector

# Brand detection
from core.brand_detect import detect_brand
from core.pixel_verify import PixelVerifier
from core.samsung_inspect import SamsungInspector
from core.generic_inspect import GenericInspector

from core.scoring import ScoringEngine
from core.report import ReportGenerator


@dataclass
class InspectionResult:

    device: object
    battery: object
    display: object
    camera: object
    cpu: object
    storage: object
    network: object
    security: object
    sensors: object
    software: object

    # Brand detection results
    brand: str          # "pixel" | "samsung" | "generic"
    brand_result: object  # PixelVerificationResult | SamsungInspectionResult | GenericInspectionResult

    score: object

    report_path: str


class Inspector:

    def __init__(self):

        self.device = DeviceInspector()
        self.battery = BatteryInspector()
        self.display = DisplayInspector()
        self.camera = CameraInspector()
        self.cpu = CpuInspector()
        self.storage = StorageInspector()
        self.network = NetworkInspector()
        self.security = SecurityInspector()
        self.sensors = SensorInspector()
        self.software = SoftwareInspector()

        # Brand-specific verifiers (instantiated once, used on demand)
        self.pixel_verifier = PixelVerifier()
        self.samsung_inspector = SamsungInspector()
        self.generic_inspector = GenericInspector()

        self.scoring = ScoringEngine()
        self.report = ReportGenerator()

    def is_connected(self) -> bool:
        return self.device.adb.is_connected()

    def inspect(self):

        print("Inspecting device...")
        device = self.device.inspect()

        print("Battery...")
        battery = self.battery.inspect()

        print("Display...")
        display = self.display.inspect()

        print("Camera...")
        camera = self.camera.inspect()

        print("CPU...")
        cpu = self.cpu.inspect()

        print("Storage...")
        storage = self.storage.inspect()

        print("Network...")
        network = self.network.inspect()

        print("Security...")
        security = self.security.inspect()

        print("Sensors...")
        sensors = self.sensors.inspect()

        print("Software...")
        software = self.software.inspect()

        # ---- Brand detection & routing ------------------------------------

        brand = detect_brand(device)

        print(f"Brand detected: {brand}")

        if brand == "pixel":
            print("Running Pixel Verification...")
            brand_result = self.pixel_verifier.verify()

        elif brand == "samsung":
            print("Running Samsung Inspection...")
            brand_result = self.samsung_inspector.inspect()

        else:
            print("Running Generic Inspection...")
            brand_result = self.generic_inspector.inspect()

        # ------------------------------------------------------------------

        print("Calculating Score...")

        score = self.scoring.calculate(
            battery=battery,
            security=security,
            storage=storage,
            display=display,
            cpu=cpu,
            camera=camera,
            sensors=sensors,
            network=network,
            brand_result=brand_result,
        )

        print("Generating Report...")

        report_path = self.report.generate(
            device=device,
            battery=battery,
            security=security,
            display=display,
            storage=storage,
            cpu=cpu,
            camera=camera,
            sensors=sensors,
            network=network,
            software=software,
            score=score,
            brand=brand,
            brand_result=brand_result,
        )

        print("Inspection Complete.")

        return InspectionResult(
            device=device,
            battery=battery,
            display=display,
            camera=camera,
            cpu=cpu,
            storage=storage,
            network=network,
            security=security,
            sensors=sensors,
            software=software,
            brand=brand,
            brand_result=brand_result,
            score=score,
            report_path=str(report_path),
        )