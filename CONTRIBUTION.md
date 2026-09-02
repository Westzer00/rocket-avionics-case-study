# Contribution Scope

This document clarifies the scope of my contribution to the 2024 GOAT avionics project.

## Project Context

- Organization: Gachon University GOAT Rocket Club
- Team: Avionics
- Year: 2024
- Platform: Raspberry Pi-based flight avionics system

## Areas I Participated In

- sensor selection and sensor-interface setup
- flight sensor data processing
- altitude-based descent / parachute deployment decision logic
- circuit and subsystem integration
- launch-vehicle integration testing
- external academic / technical events related to the GOAT project

## Team-developed Areas

The original repository contains work by multiple GOAT avionics members.
Accordingly, this repository does not present the full source tree as my individual implementation.

## Recruiting Use

For recruiting and interviews, I focus on the parts I can explain at implementation level:

1. how BMP280 / GPS / 9DOF IMU data entered the Raspberry Pi
2. why relative-altitude baseline correction was used
3. why moving-average filtering was introduced
4. how consecutive descent checks reduced false deployment
5. how the software decision was linked to GPIO / PWM actuator control
6. what was validated during launch-vehicle integration

## Accuracy Note

Experimental logic that existed in the team repository but was not active in the final verified deployment path is intentionally excluded from my claimed contribution.
