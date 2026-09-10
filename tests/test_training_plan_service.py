import json
from datetime import datetime

import pytest

from running_coach.services.training_plan_service import (
    TrainingPlanService,
)


def create_training_plan_file(
    tmp_path,
    start_date: str = "2026-09-07",
):
    training_plan_path = tmp_path / "training_plan.json"

    data = {
        "start_date": start_date,
        "weeks": [
            {
                "week": 1,
                "sessions": [
                    {
                        "session_number": 1,
                        "description": "30 Minuten Run-Walk",
                        "target_duration_min_minutes": 30,
                        "target_duration_max_minutes": 30,
                        "target_distance_min_km": None,
                        "target_distance_max_km": None,
                        "run_interval_minutes": 4,
                        "walk_interval_minutes": 1,
                        "target_effort_min": 3,
                        "target_effort_max": 4,
                        "optional": False,
                    },
                    {
                        "session_number": 2,
                        "description": "5 km locker",
                        "target_duration_min_minutes": None,
                        "target_duration_max_minutes": None,
                        "target_distance_min_km": 5.0,
                        "target_distance_max_km": 5.0,
                        "run_interval_minutes": None,
                        "walk_interval_minutes": None,
                        "target_effort_min": 3,
                        "target_effort_max": 4,
                        "optional": False,
                    },
                ],
            },
            {
                "week": 2,
                "sessions": [
                    {
                        "session_number": 1,
                        "description": "35 Minuten Run-Walk",
                        "target_duration_min_minutes": 35,
                        "target_duration_max_minutes": 35,
                        "target_distance_min_km": None,
                        "target_distance_max_km": None,
                        "run_interval_minutes": 5,
                        "walk_interval_minutes": 1,
                        "target_effort_min": 3,
                        "target_effort_max": 4,
                        "optional": False,
                    }
                ],
            },
        ],
    }

    with training_plan_path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
        )

    return training_plan_path


def create_service(tmp_path) -> TrainingPlanService:
    return TrainingPlanService(
        training_plan_path=create_training_plan_file(
            tmp_path
        )
    )


def test_get_session_returns_correct_session(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    session = service.get_session(
        week=1,
        session_number=1,
    )

    assert session.week == 1
    assert session.session_number == 1
    assert session.description == "30 Minuten Run-Walk"

    assert session.target_duration_min_minutes == 30
    assert session.target_duration_max_minutes == 30

    assert session.run_interval_minutes == 4
    assert session.walk_interval_minutes == 1

    assert session.target_effort_min == 3
    assert session.target_effort_max == 4

    assert session.optional is False


def test_get_session_returns_session_from_correct_week(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    session = service.get_session(
        week=2,
        session_number=1,
    )

    assert session.week == 2
    assert session.session_number == 1
    assert session.description == "35 Minuten Run-Walk"

    assert session.run_interval_minutes == 5
    assert session.walk_interval_minutes == 1


def test_get_session_raises_error_when_week_not_found(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    with pytest.raises(
        ValueError,
        match="Training session not found",
    ):
        service.get_session(
            week=99,
            session_number=1,
        )


def test_get_session_raises_error_when_session_not_found(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    with pytest.raises(
        ValueError,
        match="Training session not found",
    ):
        service.get_session(
            week=1,
            session_number=99,
        )


def test_get_week_for_datetime_returns_week_one(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    week = service.get_week_for_datetime(
        datetime(2026, 9, 10, 18, 30)
    )

    assert week == 1


def test_get_week_for_datetime_returns_week_one_on_sunday(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    week = service.get_week_for_datetime(
        datetime(2026, 9, 13, 23, 59)
    )

    assert week == 1


def test_get_week_for_datetime_changes_on_monday(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    week = service.get_week_for_datetime(
        datetime(2026, 9, 14, 0, 0)
    )

    assert week == 2


def test_get_week_for_datetime_counts_multiple_weeks(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    week = service.get_week_for_datetime(
        datetime(2026, 9, 14, 18, 0)
    )

    assert week == 2


def test_get_week_for_datetime_rejects_date_before_start(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    with pytest.raises(
        ValueError,
        match="before training plan start date",
    ):
        service.get_week_for_datetime(
            datetime(2026, 9, 6, 23, 59)
        )


def test_start_date_must_be_monday(
    tmp_path,
) -> None:
    training_plan_path = create_training_plan_file(
        tmp_path,
        start_date="2026-09-08",
    )

    with pytest.raises(
        ValueError,
        match="must be a Monday",
    ):
        TrainingPlanService(
            training_plan_path=training_plan_path
        )


def test_get_week_for_datetime_rejects_date_after_plan(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    with pytest.raises(
        ValueError,
        match="after training plan end date",
    ):
        service.get_week_for_datetime(
            datetime(2026, 9, 21, 12, 0)
        )

def test_get_sessions_for_week_returns_all_sessions(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    sessions = service.get_sessions_for_week(
        week=1
    )

    assert len(sessions) == 2

    assert sessions[0].week == 1
    assert sessions[0].session_number == 1
    assert sessions[0].description == "30 Minuten Run-Walk"

    assert sessions[1].week == 1
    assert sessions[1].session_number == 2
    assert sessions[1].description == "5 km locker"

def test_get_sessions_for_week_returns_sessions_from_correct_week(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    sessions = service.get_sessions_for_week(
        week=2
    )

    assert len(sessions) == 1

    assert sessions[0].week == 2
    assert sessions[0].session_number == 1
    assert sessions[0].description == "35 Minuten Run-Walk"

def test_get_sessions_for_week_raises_error_when_week_not_found(
    tmp_path,
) -> None:
    service = create_service(tmp_path)

    with pytest.raises(
        ValueError,
        match="Training week not found",
    ):
        service.get_sessions_for_week(
            week=99
        )