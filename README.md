# Pixel Inspector Pro

<div align="center">

# 🔍 Pixel Inspector Pro

### Professional Google Pixel Diagnostic & Inspection Tool

Inspect • Verify • Score • Report

Built with ❤️ by **Mustafa Shah Tech**

[Download Latest Release](https://github.com/mustafa-shah-tech/Pixel-Inspector-Pro/releases/latest)

</div>

---

## Overview

Pixel Inspector Pro is a Windows desktop application that performs a complete inspection of Google Pixel devices using ADB.

It is designed primarily for:

- Buying used Pixel phones
- Verifying authenticity
- Detecting modified or rooted devices
- Checking hardware health
- Generating professional inspection reports

---

# Features

## Device Information

- Model, Codename, Manufacturer, Serial Number
- Android Version, SDK, Build Fingerprint, Build Tags
- Security Patch, Build Date
- Kernel Version, Baseband Version, Bootloader Version
- Hardware Revision

## Pixel Verification

- Genuine Pixel check (model, codename, manufacturer)
- Tensor chip identification
- Official Google build verification
- Test-keys / custom build detection
- GSI ROM detection (system brand mismatch)
- Authenticity score with detailed issue breakdown

## Battery Analysis

- Level, Status, Health, Temperature, Voltage
- Charge Counter, Charge Full, Design Capacity
- Capacity %, Cycle Count (root-dependent)
- Charging Type, USB Current (root-dependent)
- Dedicated Battery Health Score

## CPU & Memory

- Processor, Architecture, Core Count
- Min/Max CPU Frequency, Governor
- GPU Model, GPU Frequency
- RAM Total/Available, Swap Total/Free
- Thermal Status

## Storage

- Total / Used / Free Storage
- Usage %, Filesystem, Mount Point

## Display

- Resolution, Density, Refresh Rate
- Estimated Screen Diagonal
- HDR Support, Color Space (best-effort)
- OLED Verification (heuristic, Pixel 6+)

## Camera

- Camera Count and IDs
- Front / Rear / Flash / Autofocus detection
- OIS detection
- Camera HAL Version
- Camera2 API level

## Sensors

- Accelerometer, Gyroscope, Magnetometer, Proximity, Light
- Barometer, Fingerprint, Step Counter/Detector, Heart Rate, GPS

## Network

- WiFi, Bluetooth, NFC, Mobile Data, Airplane Mode
- Carrier, SIM State, Network Type
- USB Debugging, Device IP

## Security

- Root Detection (su binary)
- Magisk, KernelSU, APatch detection
- TWRP / OrangeFox recovery detection (best-effort)
- Bootloader Lock State, Verified Boot State
- SELinux/Encryption State, OEM Unlock Support

## Software

- Installed (user) App Count, System App Count, Disabled App Count
- Google Play Services Version
- Play Protect Status

## Scoring

Every inspection receives:

- Overall Score (0-100)
- Letter Grade (A+ through F)
- Buying Recommendation
- Detailed Deductions List

Example:

```
Score: 96 / 100
Grade: A+
Recommendation:
Excellent Buy
```

---

## Reports

Pixel Inspector Pro automatically generates a full HTML inspection report covering every category above, saved to the `reports/` folder.

Future versions: PDF export, JSON export, inspection history database.

---

# Installation

### Option 1 — Download the prebuilt EXE (recommended)

Grab the latest `.exe` from [Releases](https://github.com/mustafa-shah-tech/Pixel-Inspector-Pro/releases/latest). No Python required.

### Option 2 — Run from source

Clone the repository

```bash
git clone https://github.com/mustafa-shah-tech/Pixel-Inspector-Pro.git
cd Pixel-Inspector-Pro
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

---

# Requirements

- Windows 10 / 11
- Android Platform Tools (ADB) installed and available in PATH
- USB Debugging enabled on the target Pixel device
- If running from source: Python 3.11+

---

# Known Limitations

A few data points require root access on Android 10+ and are not available on stock, unrooted devices:

- IMEI / IMEI2 / MEID
- Battery cycle count and design capacity (varies by OEM/device)
- Partition table and detailed storage health
- Pending OTA update status

These are documented in the code rather than faked or guessed.

---

# Project Structure

```
Pixel-Inspector-Pro/
│
├── core/       # ADB wrapper + all inspection modules
├── ui/         # PySide6 desktop UI
├── reports/    # Generated HTML reports (gitignored)
├── logs/       # Application logs (gitignored)
└── main.py     # Entry point
```

---

# Roadmap

- [x] Core Inspection Engine
- [x] Pixel Verification (custom ROM / GSI detection)
- [x] Root & Modification Detection (Magisk, KernelSU, APatch, TWRP, OrangeFox)
- [x] Software Inspection Module
- [x] HTML Reports
- [x] Scoring Engine
- [x] Async scanning (non-blocking UI)
- [ ] Interactive hardware tests (touchscreen, dead pixel, speaker, etc.)
- [ ] Live performance dashboard
- [ ] PDF / JSON export
- [ ] Inspection history database (SQLite)
- [ ] Companion APK for IMEI and biometric test access
- [ ] Automatic update checker
- [ ] Dark / Light themes
- [ ] Multi-language support

---

# License

MIT License — see [LICENSE](LICENSE) for details.

---

# Author

**Mustafa Shah Tech**

GitHub: https://github.com/mustafa-shah-tech

---

## Disclaimer

Pixel Inspector Pro is an independent diagnostic tool and is not affiliated with or endorsed by Google LLC.

Google, Android, and Pixel are trademarks of their respective owners.