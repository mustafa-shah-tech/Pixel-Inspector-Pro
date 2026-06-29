"""
Pixel Inspector Pro
core/inspector.py
"""

from __future__ import annotations

from dataclasses import dataclass

from core.device import DeviceInspector
from core.battery import BatteryInspector
from core.display import DisplayInspector
from core.camera import CameraInspector
from core.cpu import CPUInspector
from core.storage import StorageInspector
from core.network import NetworkInspector
from core.security import SecurityInspector
from core.sensors import SensorInspector

from core.pixel_verify import PixelVerifier

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

    pixel: object

    score: object

    report_path: str


class Inspector:

    def __init__(self):

        self.device = DeviceInspector()
        self.battery = BatteryInspector()
        self.display = DisplayInspector()
        self.camera = CameraInspector()
        self.cpu = CPUInspector()
        self.storage = StorageInspector()
        self.network = NetworkInspector()
        self.security = SecurityInspector()
        self.sensors = SensorInspector()

        self.pixel = PixelVerifier()

        self.scoring = ScoringEngine()

        self.report = ReportGenerator()

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

        print("Pixel Verification...")
        pixel = self.pixel.verify()

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
            score=score,
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
            pixel=pixel,
            score=score,
            report_path=str(report_path),
        )