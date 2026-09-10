from datetime import datetime

import pytest

from running_coach.model.run import Run


TEST_DATETIME = datetime(2026, 9, 10, 18, 30)


def test_create_valid_run() -> None:
    run = Run(
        datetime=TEST_DATETIME,
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
        walk_breaks=2,
    )

    assert run.datetime == TEST_DATETIME
    assert run.distance_km == 5.0
    assert run.duration_minutes == 40.0
    assert run.perceived_effort == 4
    assert run.walk_breaks == 2


def test_calculate_pace() -> None:
    run = Run(
        datetime=TEST_DATETIME,
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    assert run.pace_minutes_per_km == 8.0


def test_calculate_rounded_pace() -> None:
    run = Run(
        datetime=TEST_DATETIME,
        distance_km=6.0,
        duration_minutes=43.0,
        perceived_effort=4,
    )

    assert run.pace_minutes_per_km == 7.17


def test_walk_breaks_are_optional() -> None:
    run = Run(
        datetime=TEST_DATETIME,
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    assert run.walk_breaks is None


def test_distance_must_be_greater_than_zero() -> None:
    with pytest.raises(ValueError):
        Run(
            datetime=TEST_DATETIME,
            distance_km=0,
            duration_minutes=40.0,
            perceived_effort=4,
        )


def test_duration_must_be_greater_than_zero() -> None:
    with pytest.raises(ValueError):
        Run(
            datetime=TEST_DATETIME,
            distance_km=5.0,
            duration_minutes=0,
            perceived_effort=4,
        )


@pytest.mark.parametrize("effort", [0, 11])
def test_effort_must_be_between_one_and_ten(
    effort: int,
) -> None:
    with pytest.raises(ValueError):
        Run(
            datetime=TEST_DATETIME,
            distance_km=5.0,
            duration_minutes=40.0,
            perceived_effort=effort,
        )


def test_walk_breaks_cannot_be_negative() -> None:
    with pytest.raises(ValueError):
        Run(
            datetime=TEST_DATETIME,
            distance_km=5.0,
            duration_minutes=40.0,
            perceived_effort=4,
            walk_breaks=-1,
        )


def test_run_without_walk_breaks_is_valid() -> None:
    run = Run(
        datetime=TEST_DATETIME,
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    assert run.walk_breaks is None
    assert run.run_interval_minutes is None
    assert run.walk_interval_minutes is None


def test_run_with_walk_breaks_without_intervals_is_valid() -> None:
    run = Run(
        datetime=TEST_DATETIME,
        distance_km=5.0,
        duration_minutes=42.0,
        perceived_effort=4,
        walk_breaks=5,
    )

    assert run.walk_breaks == 5
    assert run.run_interval_minutes is None
    assert run.walk_interval_minutes is None


def test_run_with_walk_breaks_and_intervals_is_valid() -> None:
    run = Run(
        datetime=TEST_DATETIME,
        distance_km=5.0,
        duration_minutes=42.0,
        perceived_effort=4,
        walk_breaks=8,
        run_interval_minutes=4,
        walk_interval_minutes=1,
    )

    assert run.run_interval_minutes == 4
    assert run.walk_interval_minutes == 1


@pytest.mark.parametrize(
    ("run_interval", "walk_interval"),
    [
        (4, None),
        (None, 1),
    ],
)
def test_intervals_must_be_set_together(
    run_interval: int | None,
    walk_interval: int | None,
) -> None:
    with pytest.raises(ValueError):
        Run(
            datetime=TEST_DATETIME,
            distance_km=5.0,
            duration_minutes=42.0,
            perceived_effort=4,
            walk_breaks=5,
            run_interval_minutes=run_interval,
            walk_interval_minutes=walk_interval,
        )


@pytest.mark.parametrize(
    ("run_interval", "walk_interval"),
    [
        (0, 1),
        (-1, 1),
        (4, 0),
        (4, -1),
    ],
)
def test_intervals_must_be_positive(
    run_interval: int,
    walk_interval: int,
) -> None:
    with pytest.raises(ValueError):
        Run(
            datetime=TEST_DATETIME,
            distance_km=5.0,
            duration_minutes=42.0,
            perceived_effort=4,
            walk_breaks=5,
            run_interval_minutes=run_interval,
            walk_interval_minutes=walk_interval,
        )


def test_heart_rate_is_optional() -> None:
    run = Run(
        datetime=TEST_DATETIME,
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    assert run.average_heart_rate is None
    assert run.max_heart_rate is None


def test_valid_heart_rate_values() -> None:
    run = Run(
        datetime=TEST_DATETIME,
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
        average_heart_rate=145,
        max_heart_rate=172,
    )

    assert run.average_heart_rate == 145
    assert run.max_heart_rate == 172


@pytest.mark.parametrize("average_heart_freq", [0, -1])
def test_average_heart_freq_must_be_positive(
    average_heart_freq: int,
) -> None:
    with pytest.raises(ValueError):
        Run(
            datetime=TEST_DATETIME,
            distance_km=5.0,
            duration_minutes=40.0,
            perceived_effort=4,
            average_heart_rate=average_heart_freq,
        )


@pytest.mark.parametrize("max_heart_freq", [0, -1])
def test_max_heart_freq_must_be_positive(
    max_heart_freq: int,
) -> None:
    with pytest.raises(ValueError):
        Run(
            datetime=TEST_DATETIME,
            distance_km=5.0,
            duration_minutes=40.0,
            perceived_effort=4,
            max_heart_rate=max_heart_freq,
        )


def test_average_heart_freq_cannot_exceed_max_heart_freq() -> None:
    with pytest.raises(ValueError):
        Run(
            datetime=TEST_DATETIME,
            distance_km=5.0,
            duration_minutes=40.0,
            perceived_effort=4,
            average_heart_rate=180,
            max_heart_rate=170,
        )


def test_invalid_datetime_raises_error() -> None:
    with pytest.raises(
        ValueError,
        match="datetime must be a valid datetime object",
    ):
        Run(
            datetime="2026-09-10T18:30:00",  # type: ignore
            distance_km=5.0,
            duration_minutes=30.0,
            perceived_effort=4,
        )


def test_valid_datetime_is_accepted() -> None:
    run_datetime = datetime(2026, 9, 10, 18, 30)

    run = Run(
        datetime=run_datetime,
        distance_km=5.0,
        duration_minutes=30.0,
        perceived_effort=4,
    )

    assert run.datetime == run_datetime