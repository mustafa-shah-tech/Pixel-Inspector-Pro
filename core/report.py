"""
Pixel Inspector Pro
core/report.py
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime


class ReportGenerator:

    def __init__(self, report_dir="reports"):

        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(exist_ok=True)

    def generate(
        self,
        device,
        battery,
        security,
        display,
        storage,
        cpu,
        camera,
        sensors,
        network,
        software,
        score,
    ):

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = self.report_dir / f"Pixel_Report_{timestamp}.html"

        html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>Pixel Inspector Pro Report</title>

<style>

body {{
    font-family: Arial, Helvetica, sans-serif;
    background:#f2f2f2;
    margin:40px;
}}

.container {{
    background:white;
    padding:30px;
    border-radius:12px;
}}

table {{
    width:100%;
    border-collapse:collapse;
    margin-bottom:30px;
}}

th {{
    background:#222;
    color:white;
    padding:10px;
}}

td {{
    border:1px solid #ddd;
    padding:8px;
}}

h1 {{
    color:#222;
}}

h2 {{
    margin-top:35px;
}}

.score {{
    font-size:50px;
    font-weight:bold;
    color:#0a84ff;
}}

.good {{
    color:green;
}}

.bad {{
    color:red;
}}

.warn {{
    color:orange;
}}

</style>

</head>

<body>

<div class="container">

<h1>Pixel Inspector Pro</h1>

<p>
Inspection Date:
<b>{datetime.now().strftime("%d %B %Y %H:%M:%S")}</b>
</p>

<h2>Overall Score</h2>

<div class="score">

{score.total_score}/100

</div>

<h3>

Grade:
{score.grade}

</h3>

<h3>

Recommendation:
{score.recommendation}

</h3>

<h2>Device</h2>

<table>

<tr><th>Property</th><th>Value</th></tr>

<tr><td>Model</td><td>{device.model}</td></tr>

<tr><td>Manufacturer</td><td>{device.manufacturer}</td></tr>

<tr><td>Android</td><td>{device.android_version}</td></tr>

<tr><td>Build</td><td>{device.build_fingerprint}</td></tr>

<tr><td>Build Date</td><td>{device.build_date}</td></tr>

<tr><td>Serial</td><td>{device.serial}</td></tr>

<tr><td>Kernel</td><td>{device.kernel_version}</td></tr>

<tr><td>Baseband</td><td>{device.baseband_version}</td></tr>

<tr><td>Bootloader</td><td>{device.bootloader_version}</td></tr>

<tr><td>Hardware Rev</td><td>{device.hardware_revision}</td></tr>

</table>

<h2>Battery</h2>

<table>

<tr><th>Property</th><th>Value</th></tr>

<tr><td>Battery Level</td><td>{battery.level}%</td></tr>

<tr><td>Health</td><td>{battery.health}</td></tr>

<tr><td>Temperature</td><td>{battery.temperature} °C</td></tr>

<tr><td>Voltage</td><td>{battery.voltage} mV</td></tr>

<tr><td>Capacity</td><td>{getattr(battery,"capacity_percent","Unknown")}</td></tr>

<tr><td>Charging Type</td><td>{battery.charging_type}</td></tr>

<tr><td>USB Current</td><td>{battery.usb_current_ma if battery.usb_current_ma is not None else "N/A"} mA</td></tr>

<tr><td>Battery Score</td><td>{battery.battery_score}/100</td></tr>

</table>

<h2>Security</h2>

<table>

<tr><td>Bootloader Locked</td><td>{security.bootloader_locked}</td></tr>

<tr><td>Verified Boot</td><td>{security.verified_boot}</td></tr>

<tr><td>Rooted</td><td>{security.rooted}</td></tr>

<tr><td>Magisk</td><td>{security.magisk_installed}</td></tr>

<tr><td>Security Patch</td><td>{security.security_patch}</td></tr>

</table>

<h2>Software</h2>

<table>

<tr><th>Property</th><th>Value</th></tr>

<tr><td>Installed Apps</td><td>{software.installed_apps_count}</td></tr>

<tr><td>System Apps</td><td>{software.system_apps_count}</td></tr>

<tr><td>Disabled Apps</td><td>{software.disabled_apps_count}</td></tr>

<tr><td>Play Services</td><td>{software.play_services_version}</td></tr>

<tr><td>Play Protect</td><td>{software.play_protect_enabled}</td></tr>

<tr><td>Update Status</td><td>{software.update_status}</td></tr>

</table>

<h2>Display</h2>

<table>

<tr><td>Resolution</td><td>{display.resolution}</td></tr>

<tr><td>Density</td><td>{display.density}</td></tr>

<tr><td>Refresh Rate</td><td>{display.refresh_rate} Hz</td></tr>

<tr><td>Diagonal</td><td>{display.diagonal_inches if display.diagonal_inches is not None else "Unknown"} in</td></tr>

<tr><td>Color Space</td><td>{display.color_space}</td></tr>

<tr><td>OLED</td><td>{display.oled_verified}</td></tr>

<tr><td>HDR</td><td>{display.hdr_supported}</td></tr>

</table>

<h2>CPU</h2>

<table>

<tr><td>Processor</td><td>{cpu.processor}</td></tr>

<tr><td>Cores</td><td>{cpu.cores}</td></tr>

<tr><td>Governor</td><td>{cpu.governor}</td></tr>

<tr><td>GPU</td><td>{cpu.gpu_model}</td></tr>

<tr><td>GPU Frequency</td><td>{cpu.gpu_frequency_mhz} MHz</td></tr>

<tr><td>Total RAM</td><td>{cpu.total_ram_gb} GB</td></tr>

<tr><td>Available RAM</td><td>{cpu.available_ram_gb} GB</td></tr>

<tr><td>Swap Total</td><td>{cpu.swap_total_gb} GB</td></tr>

<tr><td>Swap Free</td><td>{cpu.swap_free_gb} GB</td></tr>

<tr><td>Thermal</td><td>{cpu.thermal_status}</td></tr>

</table>

<h2>Storage</h2>

<table>

<tr><td>Total</td><td>{storage.total_gb} GB</td></tr>

<tr><td>Used</td><td>{storage.used_gb} GB</td></tr>

<tr><td>Free</td><td>{storage.free_gb} GB</td></tr>

<tr><td>Usage</td><td>{storage.usage_percent}%</td></tr>

</table>

<h2>Camera</h2>

<table>

<tr><td>Cameras</td><td>{camera.camera_count}</td></tr>

<tr><td>Front Camera</td><td>{camera.has_front_camera}</td></tr>

<tr><td>Rear Camera</td><td>{camera.has_back_camera}</td></tr>

<tr><td>Flash</td><td>{camera.has_flash}</td></tr>

<tr><td>Autofocus</td><td>{camera.has_autofocus}</td></tr>

<tr><td>OIS</td><td>{camera.has_ois}</td></tr>

<tr><td>HAL Version</td><td>{camera.camera_hal_version if camera.camera_hal_version else "Unknown"}</td></tr>

</table>

<h2>Sensors</h2>

<table>

<tr><td>Total Sensors</td><td>{sensors.total_sensors}</td></tr>

<tr><td>Fingerprint</td><td>{sensors.fingerprint}</td></tr>

<tr><td>Accelerometer</td><td>{sensors.accelerometer}</td></tr>

<tr><td>Gyroscope</td><td>{sensors.gyroscope}</td></tr>

<tr><td>Proximity</td><td>{sensors.proximity}</td></tr>

<tr><td>Light</td><td>{sensors.light}</td></tr>

</table>

<h2>Network</h2>

<table>

<tr><td>Carrier</td><td>{network.carrier}</td></tr>

<tr><td>WiFi</td><td>{network.wifi_enabled}</td></tr>

<tr><td>Bluetooth</td><td>{network.bluetooth_enabled}</td></tr>

<tr><td>USB Debugging</td><td>{network.usb_debugging}</td></tr>

<tr><td>IP Address</td><td>{network.device_ip}</td></tr>

</table>

<h2>Deductions</h2>

<ul>

{''.join(f'<li>{d}</li>' for d in score.deductions)}

</ul>

</div>

</body>

</html>
"""

        filename.write_text(html, encoding="utf-8")

        return filename