# System Architecture

## High-Level Flow

```text
BMP280 (Altitude) --I2C--┐
NEO-M8N GPS ------UART---┼--> Raspberry Pi
EBIMU 9DOF -------UART---┘
                           |
                           v
                    Sensor acquisition
                           |
                           v
                   Altitude preprocessing
                           |
                           v
                   Descent-state decision
                           |
                           v
                     GPIO / PWM
                           |
                           v
                     Relay / Servo
                           |
                           v
                Parachute deployment
```

## Sensor Interfaces

| Sensor | Purpose | Interface | Main Data |
|---|---|---|---|
| BMP280 | altitude | I2C | altitude |
| NEO-M8N GPS | position | UART / Serial | latitude / longitude |
| EBIMU 9DOF | attitude / motion | UART / Serial | roll / pitch / yaw and xyz values |

## Runtime Structure

The original system separated sensor acquisition using multiprocessing processes and queues.
This allowed BMP, GPS, and IMU acquisition to run independently while the main process consumed the latest values for storage and decision logic.

## Design Intent

The architecture follows a simple embedded-system loop:

**sense → preprocess → decide → actuate → log**
