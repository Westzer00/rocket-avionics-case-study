# Rocket Avionics & Parachute Deployment System

> 2024 Gachon University GOAT Avionics Team — recruiting-oriented personal case study

This repository documents my 2024 participation in the GOAT rocket avionics project.
The original system was developed collaboratively by the GOAT avionics team; this repository focuses on the parts I can explain and defend in interviews: **sensor integration, flight-data processing, altitude-based descent detection, actuator linkage, and launch-vehicle integration testing**.

## Overview

The avionics system collected flight data from multiple sensors on a Raspberry Pi and used altitude trends to determine whether the rocket was descending.
When the deployment condition was satisfied, the software linked the decision result to a relay/servo actuator path for parachute deployment.

```text
BMP280 (Altitude) ── I2C ──┐
NEO-M8N GPS ─────── UART ──┼──> Raspberry Pi
EBIMU 9DOF ──────── UART ──┘
                              │
                              v
                       Sensor Processing
                              │
                              v
                       Descent Detection
                              │
                              v
                       GPIO / PWM Output
                              │
                              v
                       Relay / Servo
                              │
                              v
                    Parachute Deployment
```

## My Contribution

- Participated in **sensor selection and sensor-interface integration**
- Worked on **flight sensor data processing**
- Developed and validated **altitude-based parachute deployment decision logic**
- Participated in **circuit/system integration and launch-vehicle testing**
- Participated in the **2024 KSPE Spring Conference NURA session (Jeju)** and the **National University Rocket Conference (Daejeon)**

> This was a team project. I do **not** claim sole ownership of the full avionics codebase.

## Technical Stack

- **Platform:** Raspberry Pi
- **Language:** Python
- **Sensors:** BMP280, NEO-M8N GPS, EBIMU 9DOF
- **Interfaces:** I2C, UART / Serial
- **Control:** GPIO, PWM, Relay, Servo
- **Data:** MySQL / multiprocessing Queue-based data flow

## Key Logic

### 1. Sensor Initialization and Baseline Correction
For altitude data, multiple initial samples were averaged to establish a launch-site baseline.
This reduced the impact of absolute elevation and startup noise when using relative altitude during flight.

### 2. Moving-Average Descent Detection
The deployment logic used a moving average instead of a single raw altitude sample.

The team implementation used:
- moving-average window: **10 samples**
- minimum deployment altitude: **100 m**
- descent confirmation: **5 consecutive downward checks**

A simplified interview-oriented example is available in [`examples/descent_detector.py`](examples/descent_detector.py).

### 3. Actuator Linkage
The final descent decision was connected to Raspberry Pi GPIO/PWM output controlling a relay and servo used in the parachute deployment mechanism.

## What Was *Not* Used as a Final Deployment Trigger

The codebase also contained experimental/unfinished logic related to:
- IMU attitude-based deployment
- position / critical-area logic

These were **not active final deployment triggers** in the verified flight code, so this case study does not present them as completed production features.

## Repository Structure

```text
.
├── README.md
├── CONTRIBUTION.md
├── docs/
│   ├── architecture.md
│   └── deployment-logic.md
├── examples/
│   └── descent_detector.py
└── assets/
    └── README.md
```

## Original Team Repository

Original GOAT team repository: **AvionicsOfGOAT/2024-avionics-and-ground-system**

This personal repository is intentionally a **case study**, not a copy of the full team repository.
