import pytest

from running_coach.model.training_session import TrainingSession


def test_create_valid_training_session() -> None:
    session = TrainingSession(
        week=1,
        session_number=1,
        description="Lockerer Run-Walk-Lauf",
        target_duration_minutes=30,
        run_interval_minutes=4,
        walk_interval_minutes=1,
        target_effort_min=3,
        target_effort_max=4,
    )

    assert session.week == 1
    assert session.session_number == 1
    assert session.description == "Lockerer Run-Walk-Lauf"
    assert session.target_duration_minutes == 30
    assert session.run_interval_minutes == 4
    assert session.walk_interval_minutes == 1
    assert session.target_effort_min == 3
    assert session.target_effort_max == 4
    assert session.optional is False


def test_optional_training_session() -> None:
    session = TrainingSession(
        week=1,
        session_number=3,
        description="Sehr lockerer Lauf",
        target_duration_minutes=30,
        optional=True,
    )

    assert session.optional is True


@pytest.mark.parametrize("week", [0, -1])
def test_week_must_be_greater_than_zero(week: int) -> None:
    with pytest.raises(ValueError):
        TrainingSession(
            week=week,
            session_number=1,
            description="Test",
        )


@pytest.mark.parametrize("session_number", [0, -1])
def test_session_number_must_be_greater_than_zero(
    session_number: int,
) -> None:
    with pytest.raises(ValueError):
        TrainingSession(
            week=1,
            session_number=session_number,
            description="Test",
        )


@pytest.mark.parametrize("description", ["", "   "])
def test_description_cannot_be_empty(description: str) -> None:
    with pytest.raises(ValueError):
        TrainingSession(
            week=1,
            session_number=1,
            description=description,
        )


@pytest.mark.parametrize("duration", [0, -1])
def test_target_duration_must_be_positive(duration: int) -> None:
    with pytest.raises(ValueError):
        TrainingSession(
            week=1,
            session_number=1,
            description="Test",
            target_duration_minutes=duration,
        )


@pytest.mark.parametrize("distance", [0, -1.0])
def test_target_distance_must_be_positive(distance: float) -> None:
    with pytest.raises(ValueError):
        TrainingSession(
            week=1,
            session_number=1,
            description="Test",
            target_distance_km=distance,
        )


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
        TrainingSession(
            week=1,
            session_number=1,
            description="Test",
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
        TrainingSession(
            week=1,
            session_number=1,
            description="Test",
            run_interval_minutes=run_interval,
            walk_interval_minutes=walk_interval,
        )


@pytest.mark.parametrize(
    ("effort_min", "effort_max"),
    [
        (3, None),
        (None, 4),
    ],
)
def test_effort_range_must_be_set_together(
    effort_min: int | None,
    effort_max: int | None,
) -> None:
    with pytest.raises(ValueError):
        TrainingSession(
            week=1,
            session_number=1,
            description="Test",
            target_effort_min=effort_min,
            target_effort_max=effort_max,
        )


@pytest.mark.parametrize(
    ("effort_min", "effort_max"),
    [
        (0, 4),
        (11, 11),
        (3, 0),
        (3, 11),
    ],
)
def test_effort_range_must_be_between_one_and_ten(
    effort_min: int,
    effort_max: int,
) -> None:
    with pytest.raises(ValueError):
        TrainingSession(
            week=1,
            session_number=1,
            description="Test",
            target_effort_min=effort_min,
            target_effort_max=effort_max,
        )


def test_effort_min_cannot_be_greater_than_effort_max() -> None:
    with pytest.raises(ValueError):
        TrainingSession(
            week=1,
            session_number=1,
            description="Test",
            target_effort_min=6,
            target_effort_max=4,
        )