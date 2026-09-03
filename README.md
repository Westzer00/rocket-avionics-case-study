# 🚀 Rocket Avionics & Parachute Deployment System 🚀

> **2024 가천대학교 로켓동아리 GOAT 전자부 — 취업용 개인 Case Study**

2024년 GOAT 로켓 Avionics 프로젝트에서 수행한 내용을 취업용으로 정리한 저장소입니다.

전체 시스템은 **GOAT 전자부 팀 공동개발**이며, 이 저장소에서는 제가 면접에서 구현 수준으로 설명할 수 있는  
**센서 연동 → 비행 데이터 처리 → 고도 기반 하강 판단 → 낙하산 전개 장치 제어 → 실제 발사체 통합 테스트**를 중심으로 정리했습니다.

---

## 1. 프로젝트 개요

BMP280·GPS·9DOF IMU에서 비행 데이터를 수집하고 Raspberry Pi에서 처리한 뒤,  
**고도 변화로 하강 상태를 판단하여 Relay/Servo 기반 낙하산 전개 장치를 제어하는 비행전자 시스템**입니다.

```text
BMP280 (고도) ───── I2C ──┐
NEO-M8N GPS ────── UART ──┼──> Raspberry Pi
EBIMU 9DOF ─────── UART ──┘
                              │
                              ▼
                        Sensor Processing
                              │
                              ▼
                         Descent Detection
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

---

## 2. 담당 역할

- 비행에 사용할 **센서 선정 및 인터페이스 연동**
- BMP280·GPS·9DOF IMU의 **센서 데이터 수집·처리**
- **고도 기반 낙하산 사출 판단 로직 개발·검증**
- 회로 및 전자부 시스템 통합
- 실제 발사체 통합 테스트 참여
- **2024 한국추진공학회 춘계학술대회 NURA 세션(제주)** 참가
- **전국대학교로켓학술대회(대전)** 참가

> 본 프로젝트는 팀 프로젝트이며, 전체 Avionics 코드의 단독 개발을 주장하지 않습니다.

---

## 3. 기술 스택

| 구분 | 기술 |
|---|---|
| Platform | Raspberry Pi |
| Language | Python |
| Sensors | BMP280, NEO-M8N GPS, EBIMU 9DOF |
| Communication | I2C, UART / Serial |
| Control | GPIO, PWM, Relay, Servo |
| Data | MySQL, multiprocessing Queue |

---

## 4. 센서 구성

| 센서 | 용도 | 인터페이스 | 주요 데이터 |
|---|---|---|---|
| BMP280 | 고도 측정 | I2C | altitude |
| NEO-M8N GPS | 위치 측정 | UART / Serial | latitude, longitude |
| EBIMU 9DOF | 자세/운동 정보 | UART / Serial | roll, pitch, yaw, xyz |

센서별 데이터 수집은 별도 Process와 Queue를 활용하는 구조로 구성되어,  
메인 로직에서 최신 센서값을 받아 저장 및 상태판단에 사용할 수 있도록 했습니다.

---

## 5. 고도 초기값 보정

발사 직후 센서의 순간적인 흔들림과 발사지점의 절대고도 영향을 줄이기 위해  
초기 고도값을 여러 번 측정해 평균을 구하고 이를 기준고도로 사용했습니다.

```text
상대 고도 = 현재 측정 고도 - 초기 기준 고도
```

이를 통해 발사지점을 기준으로 비행 중 고도 변화를 판단할 수 있도록 했습니다.

---

## 6. 고도 기반 하강 판단

단일 고도값이 순간적으로 감소했다고 바로 사출하지 않고,  
**Moving Average + 연속 하강 확인 조건**을 적용했습니다.

```text
Raw Altitude
     │
     ▼
유효 범위 확인
     │
     ▼
최근 10개 Moving Average
     │
     ▼
사출 가능 고도(100m 이상) 확인
     │
     ▼
이전 평균 > 현재 평균 ?
     │
     ▼
연속 하강 Count 증가
     │
     ▼
5회 연속 하강 확인
     │
     ▼
Deployment Decision
```

팀 코드에서 확인되는 주요 조건은 다음과 같습니다.

| 항목 | 값 |
|---|---:|
| Moving Average Window | 10 samples |
| Minimum Deployment Altitude | 100 m |
| Falling Confirmation | 5 consecutive checks |

이 구조는 진동이나 센서 노이즈로 인해 고도값이 한 번 튀는 상황에서  
낙하산이 잘못 전개될 가능성을 줄이기 위한 판단 방식입니다.

간소화한 예제 코드는 [`examples/descent_detector.py`](examples/descent_detector.py)에서 확인할 수 있습니다.

---

## 7. Actuator 제어

하강 상태가 확정되면 판단 결과를 Raspberry Pi의 **GPIO/PWM 출력**과 연결해  
Relay와 Servo를 이용한 낙하산 전개 장치를 제어하도록 구성했습니다.

```text
Descent Detection
        │
        ▼
       GPIO
      /    \
   Relay   PWM
            │
            ▼
          Servo
            │
            ▼
   Parachute Deployment
```

---

## 8. 최종 사출 조건으로 사용하지 않은 기능

원본 팀 코드에는 다음 기능의 구현 흔적도 존재합니다.

- IMU 자세 기반 사출 판단
- GPS/위치 기반 Critical Area 판단

하지만 확인한 최종 코드에서는 해당 경로가 **실제 최종 사출 Trigger로 활성화되어 있지 않았기 때문에**,  
이 저장소에서는 완성 기능으로 주장하지 않습니다.

---

## 9. Repository 구성

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

---

## 10. 원본 팀 Repository

전체 프로젝트 원본은 GOAT 전자부 팀 Repository에서 확인할 수 있습니다.

**AvionicsOfGOAT/2024-avionics-and-ground-system**
https://github.com/AvionicsOfGOAT 

이 저장소는 팀 코드를 복제하기 위한 목적이 아니라,  
**개인 담당 영역과 시스템 이해도를 설명하기 위한 취업용 Case Study**입니다.

---

## 11. 추가 예정 자료

공개 가능한 범위에서 다음 자료를 추가할 예정입니다.

- 실제 로켓/발사 사진
- Avionics 조립 사진
- 센서/배선 사진
- 제주 한국추진공학회 참가 사진
- 대전 로켓학술대회 참가 사진
