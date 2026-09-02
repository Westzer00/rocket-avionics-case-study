"""Simplified altitude-based descent detector.

Interview-oriented reconstruction of the verified decision structure used in
the 2024 GOAT avionics project. This is not a copy of the full team source.
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
        if not self.min_valid_altitude <= altitude <= self.max_valid_altitude:
            return DetectionResult(self.previous_average, self.falling_count, False)

        self.history.append(altitude)
        if len(self.history) < self.window_size:
            return DetectionResult(None, self.falling_count, False)

        current_average = sum(self.history) / len(self.history)

        if current_average < self.min_deploy_altitude:
            self.falling_count = 0
            self.previous_average = current_average
            return DetectionResult(current_average, 0, False)

        if self.previous_average is not None and current_average < self.previous_average:
            self.falling_count += 1
        else:
            self.falling_count = 0

        self.previous_average = current_average
        deploy = self.falling_count >= self.confirmation_count
        return DetectionResult(current_average, self.falling_count, deploy)


if __name__ == "__main__":
    detector = DescentDetector()
    demo_altitudes = [120, 123, 126, 130, 134, 137, 140, 142, 143, 144,
                      143, 142, 141, 140, 139, 138, 137, 136, 135, 134]
    for sample in demo_altitudes:
        result = detector.update(sample)
        print(sample, result)
