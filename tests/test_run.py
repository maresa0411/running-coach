import pytest

from running_coach.model.run import Run

def test_create_valid_run() -> None:
    run = Run(
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
        walk_breaks=2,
    )

    assert run.distance_km == 5.0
    assert run.duration_minutes == 40.0
    assert run.perceived_effort == 4
    assert run.walk_breaks == 2


def test_calculate_pace() -> None:
    run = Run(
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    assert run.pace_minutes_per_km == 8.0


def test_walk_breaks_are_optional() -> None:
    run = Run(
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    assert run.walk_breaks is None


def test_distance_must_be_greater_than_zero() -> None:
    with pytest.raises(ValueError):
        Run(
            distance_km=0,
            duration_minutes=40.0,
            perceived_effort=4,
        )


def test_duration_must_be_greater_than_zero() -> None:
    with pytest.raises(ValueError):
        Run(
            distance_km=5.0,
            duration_minutes=0,
            perceived_effort=4,
        )


@pytest.mark.parametrize("effort", [0, 11])
def test_effort_must_be_between_one_and_ten(effort: int) -> None:
    with pytest.raises(ValueError):
        Run(
            distance_km=5.0,
            duration_minutes=40.0,
            perceived_effort=effort,
        )

def test_walk_breaks_cannot_be_negative() -> None:
    with pytest.raises(ValueError):
        Run(
            distance_km=5.0,
            duration_minutes=40.0,
            perceived_effort=4,
            walk_breaks=-1,
        )

def test_run_without_walk_breaks_is_valid() -> None:
    run = Run(
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    assert run.walk_breaks is None
    assert run.run_interval_minutes is None
    assert run.walk_interval_minutes is None


def test_run_with_walk_breaks_without_intervals_is_valid() -> None:
    run = Run(
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
            distance_km=5.0,
            duration_minutes=42.0,
            perceived_effort=4,
            walk_breaks=5,
            run_interval_minutes=run_interval,
            walk_interval_minutes=walk_interval,
        )


def test_intervals_require_walk_breaks() -> None:
    with pytest.raises(ValueError):
        Run(
            distance_km=5.0,
            duration_minutes=40.0,
            perceived_effort=4,
            run_interval_minutes=4,
            walk_interval_minutes=1,
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
            distance_km=5.0,
            duration_minutes=42.0,
            perceived_effort=4,
            walk_breaks=5,
            run_interval_minutes=run_interval,
            walk_interval_minutes=walk_interval,
        )