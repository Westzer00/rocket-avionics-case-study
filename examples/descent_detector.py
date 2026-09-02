"""고도 기반 하강 판단 로직의 간소화 예제.

2024 GOAT 팀 코드에서 확인되는 판단 구조를 면접 설명용으로 재구성한 코드입니다.
원본 팀 전체 코드를 그대로 복사한 것이 아닙니다.
"""

from collections import deque
from dataclasses import dataclass


@dataclass
class DetectionResult:
    moving_average: float | None
    falling_count: int
    deploy: bool


class DescentDetector:
    def __init__(
        self,
        window_size: int = 10,
        confirmation_count: int = 5,
        min_deploy_altitude: float = 100.0,
        min_valid_altitude: float = -10.0,
        max_valid_altitude: float = 400.0,
    ) -> None:
        self.window_size = window_size
        self.confirmation_count = confirmation_count
        self.min_deploy_altitude = min_deploy_altitude
        self.min_valid_altitude = min_valid_altitude
        self.max_valid_altitude = max_valid_altitude

        self.history = deque(maxlen=window_size)
        self.previous_average = None
        self.falling_count = 0

    def update(self, altitude: float) -> DetectionResult:
        # 1. 비정상 고도값 제외
        if not self.min_valid_altitude <= altitude <= self.max_valid_altitude:
            return DetectionResult(
                self.previous_average,
                self.falling_count,
                False,
            )

        # 2. 최근 고도값 저장
        self.history.append(altitude)

        # Moving Average 계산에 필요한 데이터가 아직 부족한 경우
        if len(self.history) < self.window_size:
            return DetectionResult(None, self.falling_count, False)

        current_average = sum(self.history) / len(self.history)

        # 3. 사출 허용 최소고도 조건
        if current_average < self.min_deploy_altitude:
            self.falling_count = 0
            self.previous_average = current_average
            return DetectionResult(current_average, 0, False)

        # 4. 이전 평균보다 현재 평균이 낮으면 하강 Count 증가
        if (
            self.previous_average is not None
            and current_average < self.previous_average
        ):
            self.falling_count += 1
        else:
            self.falling_count = 0

        self.previous_average = current_average

        # 5. 연속 하강 횟수 충족 시 사출 판단
        deploy = self.falling_count >= self.confirmation_count

        return DetectionResult(
            current_average,
            self.falling_count,
            deploy,
        )


if __name__ == "__main__":
    detector = DescentDetector()

    demo_altitudes = [
        120, 123, 126, 130, 134,
        137, 140, 142, 143, 144,
        143, 142, 141, 140, 139,
        138, 137, 136, 135, 134,
    ]

    for sample in demo_altitudes:
        result = detector.update(sample)
        print(sample, result)
