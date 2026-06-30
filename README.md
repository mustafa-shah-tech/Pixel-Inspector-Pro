# Pixel Inspector Pro

<div align="center">

# 🔍 Pixel Inspector Pro

### Professional Google Pixel Diagnostic & Inspection Tool

Inspect • Verify • Score • Report

Built with ❤️ by **Mustafa Shah Tech**

</div>

---

## Overview

Pixel Inspector Pro is a Windows desktop application that performs a complete inspection of Google Pixel devices using ADB.

It is designed primarily for:

- Buying used Pixel phones
- Verifying authenticity
- Detecting modified devices
- Checking hardware health
- Generating professional inspection reports

---

# Features

## Device Information

- Model
- Codename
- Manufacturer
- Android Version
- Build ID
- Build Fingerprint
- Serial Number

---

## Battery Analysis

- Battery Level
- Charging Status
- Health
- Temperature
- Voltage
- Charge Counter
- Cycle Count
- Estimated Battery Capacity

---

## Display

- Resolution
- Density
- Refresh Rate
- HDR Support

---

## CPU

- Processor
- RAM
- Architecture
- Core Count

---

## Storage

- Total Storage
- Used Storage
- Free Storage
- Usage %

---

## Camera

- Camera Count
- Front Camera
- Rear Camera
- Flash
- Autofocus

---

## Sensors

- Fingerprint
- Gyroscope
- Accelerometer
- Ambient Light
- Proximity

---

## Security

- Root Detection
- Magisk Detection
- Bootloader Lock
- Verified Boot
- Security Patch

---

## Network

- WiFi
- Bluetooth
- Carrier
- USB Debugging
- Device IP

---

## Pixel Verification

- Genuine Pixel Check
- Model Verification
- Codename Verification
- Tensor Chip Verification
- Official Build Verification
- Authenticity Score

---

## Scoring

Each inspection receives:

- Overall Score
- Grade
- Recommendation
- Detailed deductions

Example:

```
Score: 96 / 100

Grade: A+

Recommendation:
Excellent Buy
```

---

## Reports

Pixel Inspector Pro automatically generates:

- HTML Report

Future versions:

- PDF
- JSON
- Database History

---

# Installation

Clone the repository

```bash
git clone https://github.com/mustafa-shah-tech/Pixel-Inspector-Pro.git
```

Enter the project

```bash
cd PixelInspectorPro
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

- Windows 10 / 11
- Python 3.11+
- Android Platform Tools (ADB)
- USB Debugging Enabled

---

# Running

```bash
python main.py
```

---

# Project Structure

```
PixelInspectorPro/
│
├── core/
├── ui/
├── assets/
├── reports/
├── database/
└── logs/
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