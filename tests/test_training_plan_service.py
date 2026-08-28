import json

import pytest

from running_coach.services.training_plan_service import TrainingPlanService


def test_get_session_returns_training_session(tmp_path) -> None:
    training_plan = {
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
                    }
                ],
            }
        ]
    }

    training_plan_path = tmp_path / "training_plan.json"

    training_plan_path.write_text(
        json.dumps(training_plan),
        encoding="utf-8",
    )

    service = TrainingPlanService(
        training_plan_path=training_plan_path
    )

    session = service.get_session(
        week=1,
        session_number=1,
    )

    assert session.week == 1
    assert session.session_number == 1
    assert session.description == "30 Minuten Run-Walk"
    assert session.target_duration_min_minutes == 30
    assert session.target_duration_max_minutes == 30
    assert session.target_distance_min_km is None
    assert session.target_distance_max_km is None
    assert session.run_interval_minutes == 4
    assert session.walk_interval_minutes == 1
    assert session.target_effort_min == 3
    assert session.target_effort_max == 4
    assert session.optional is False


def test_get_session_returns_correct_session(tmp_path) -> None:
    training_plan = {
        "weeks": [
            {
                "week": 1,
                "sessions": [
                    {
                        "session_number": 1,
                        "description": "Einheit 1",
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
                        "description": "Einheit 2",
                        "target_duration_min_minutes": None,
                        "target_duration_max_minutes": None,
                        "target_distance_min_km": 5.0,
                        "target_distance_max_km": 5.5,
                        "run_interval_minutes": None,
                        "walk_interval_minutes": None,
                        "target_effort_min": 3,
                        "target_effort_max": 4,
                        "optional": False,
                    },
                ],
            }
        ]
    }

    training_plan_path = tmp_path / "training_plan.json"

    training_plan_path.write_text(
        json.dumps(training_plan),
        encoding="utf-8",
    )

    service = TrainingPlanService(
        training_plan_path=training_plan_path
    )

    session = service.get_session(
        week=1,
        session_number=2,
    )

    assert session.session_number == 2
    assert session.description == "Einheit 2"
    assert session.target_distance_min_km == 5.0
    assert session.target_distance_max_km == 5.5


def test_get_session_returns_correct_week(tmp_path) -> None:
    training_plan = {
        "weeks": [
            {
                "week": 1,
                "sessions": [
                    {
                        "session_number": 1,
                        "description": "Woche 1",
                        "target_duration_min_minutes": 30,
                        "target_duration_max_minutes": 30,
                        "target_distance_min_km": None,
                        "target_distance_max_km": None,
                        "run_interval_minutes": None,
                        "walk_interval_minutes": None,
                        "target_effort_min": 3,
                        "target_effort_max": 4,
                        "optional": False,
                    }
                ],
            },
            {
                "week": 2,
                "sessions": [
                    {
                        "session_number": 1,
                        "description": "Woche 2",
                        "target_duration_min_minutes": 30,
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
        ]
    }

    training_plan_path = tmp_path / "training_plan.json"

    training_plan_path.write_text(
        json.dumps(training_plan),
        encoding="utf-8",
    )

    service = TrainingPlanService(
        training_plan_path=training_plan_path
    )

    session = service.get_session(
        week=2,
        session_number=1,
    )

    assert session.week == 2
    assert session.description == "Woche 2"
    assert session.target_duration_min_minutes == 30
    assert session.target_duration_max_minutes == 35


def test_get_session_raises_error_when_week_does_not_exist(
    tmp_path,
) -> None:
    training_plan = {
        "weeks": [
            {
                "week": 1,
                "sessions": [],
            }
        ]
    }

    training_plan_path = tmp_path / "training_plan.json"

    training_plan_path.write_text(
        json.dumps(training_plan),
        encoding="utf-8",
    )

    service = TrainingPlanService(
        training_plan_path=training_plan_path
    )

    with pytest.raises(
        ValueError,
        match="Training session not found",
    ):
        service.get_session(
            week=2,
            session_number=1,
        )


def test_get_session_raises_error_when_session_does_not_exist(
    tmp_path,
) -> None:
    training_plan = {
        "weeks": [
            {
                "week": 1,
                "sessions": [],
            }
        ]
    }

    training_plan_path = tmp_path / "training_plan.json"

    training_plan_path.write_text(
        json.dumps(training_plan),
        encoding="utf-8",
    )

    service = TrainingPlanService(
        training_plan_path=training_plan_path
    )

    with pytest.raises(
        ValueError,
        match="Training session not found",
    ):
        service.get_session(
            week=1,
            session_number=99,
        )