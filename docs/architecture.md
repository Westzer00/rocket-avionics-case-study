# 시스템 구조 (System Architecture)

## 전체 흐름

```text
BMP280 (고도) ----- I2C ---┐
NEO-M8N GPS ------- UART --┼--> Raspberry Pi
EBIMU 9DOF -------- UART --┘
                              │
                              ▼
                       Sensor Acquisition
                              │
                              ▼
                       Data Processing
                              │
                              ▼
                    Descent-state Decision
                              │
                              ▼
                         GPIO / PWM
                              │
                              ▼
                         Relay / Servo
                              │
                              ▼
                    Parachute Deployment
```

## 센서 인터페이스

| 센서 | 목적 | 통신 | 데이터 |
|---|---|---|---|
| BMP280 | 고도 | I2C | altitude |
| NEO-M8N GPS | 위치 | UART / Serial | latitude / longitude |
| EBIMU 9DOF | 자세/운동 | UART / Serial | roll / pitch / yaw, xyz |

## Runtime 구조

원본 시스템은 BMP, GPS, IMU 센서 데이터를 각각 별도의 Process에서 수집하고  
Queue를 통해 메인 Process로 전달하는 구조를 사용했습니다.

메인 Process에서는 전달받은 데이터를 저장하고, 특히 고도값은 하강 판단 로직의 입력으로 사용했습니다.

## 핵심 구조

이 프로젝트는 Embedded/Robotics SW 관점에서 다음 흐름을 경험한 프로젝트입니다.

**Sense → Preprocess → Decide → Actuate → Log**
