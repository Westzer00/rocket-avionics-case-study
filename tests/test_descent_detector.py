"""Independent example tests: no real hardware, GPIO or flight input required."""
from examples.descent_detector import DescentDetector


def test_deployment_requires_five_consecutive_descents():
    detector = DescentDetector()
    for _ in range(10):
        detector.update(150)
    results = [detector.update(a) for a in (149, 148, 147, 146, 145)]
    assert not any(result.deploy for result in results[:4])
    assert results[4].deploy
    assert results[4].falling_count == 5


def test_single_noisy_drop_does_not_deploy():
    detector = DescentDetector()
    for _ in range(10):
        detector.update(150)
    for altitude in (149, 150, 149, 150):
        result = detector.update(altitude)
        assert result.deploy is False
    assert result.falling_count == 0


def test_below_minimum_deployment_altitude():
    detector = DescentDetector()
    for altitude in [50] * 10 + [49, 48, 47, 46, 45, 44]:
        result = detector.update(altitude)
        assert result.deploy is False
    assert result.falling_count == 0


def test_invalid_sensor_value_is_ignored():
    detector = DescentDetector()
    for _ in range(10):
        detector.update(150)
    result = detector.update(999)
    assert result.deploy is False
    assert result.moving_average == 150

def test_deployment_event_is_emitted_only_once():
    detector = DescentDetector()
    for _ in range(10):
        detector.update(150)
    results = [detector.update(value) for value in range(149, 135, -1)]
    assert sum(int(result.deploy) for result in results) == 1
    assert detector.deployment_latched is True

def test_invalid_reading_after_deployment_does_not_retrigger():
    detector = DescentDetector()
    for _ in range(10):
        detector.update(150)
    for value in (149, 148, 147, 146, 145):
        detector.update(value)
    for value in (999, 120, 115):
        assert detector.update(value).deploy is False
