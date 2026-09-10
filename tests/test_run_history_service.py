import json
from datetime import datetime

from running_coach.model.run import Run
from running_coach.services.run_history_service import (
    RunHistoryService,
)


def test_get_runs_returns_empty_list_when_file_does_not_exist(
    tmp_path,
) -> None:
    service = RunHistoryService(
        runs_path=tmp_path / "runs.json"
    )

    runs = service.get_runs()

    assert runs == []


def test_add_run_creates_file_and_saves_run(
    tmp_path,
) -> None:
    runs_path = tmp_path / "runs.json"

    service = RunHistoryService(
        runs_path=runs_path
    )

    run = Run(
        datetime=datetime(2026, 9, 10, 18, 30),
        distance_km=5.0,
        duration_minutes=32.0,
        perceived_effort=4,
        walk_breaks=6,
        run_interval_minutes=4,
        walk_interval_minutes=1,
        average_heart_rate=145,
        max_heart_rate=162,
    )

    service.add_run(run)

    assert runs_path.exists()

    with runs_path.open(
        mode="r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    assert len(data) == 1

    assert data[0]["datetime"] == "2026-09-10T18:30:00"
    assert data[0]["distance_km"] == 5.0
    assert data[0]["duration_minutes"] == 32.0
    assert data[0]["perceived_effort"] == 4
    assert data[0]["walk_breaks"] == 6
    assert data[0]["run_interval_minutes"] == 4
    assert data[0]["walk_interval_minutes"] == 1
    assert data[0]["average_heart_rate"] == 145
    assert data[0]["max_heart_rate"] == 162


def test_get_runs_loads_saved_run(
    tmp_path,
) -> None:
    runs_path = tmp_path / "runs.json"

    data = [
        {
            "datetime": "2026-09-10T18:30:00",
            "distance_km": 5.0,
            "duration_minutes": 32.0,
            "perceived_effort": 4,
            "walk_breaks": 6,
            "run_interval_minutes": 4,
            "walk_interval_minutes": 1,
            "average_heart_rate": 145,
            "max_heart_rate": 162,
        }
    ]

    with runs_path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        json.dump(data, file)

    service = RunHistoryService(
        runs_path=runs_path
    )

    runs = service.get_runs()

    assert len(runs) == 1

    run = runs[0]

    assert run.datetime == datetime(
        2026,
        9,
        10,
        18,
        30,
    )
    assert run.distance_km == 5.0
    assert run.duration_minutes == 32.0
    assert run.perceived_effort == 4
    assert run.walk_breaks == 6
    assert run.run_interval_minutes == 4
    assert run.walk_interval_minutes == 1
    assert run.average_heart_rate == 145
    assert run.max_heart_rate == 162


def test_add_run_preserves_existing_runs(
    tmp_path,
) -> None:
    runs_path = tmp_path / "runs.json"

    service = RunHistoryService(
        runs_path=runs_path
    )

    first_run = Run(
        datetime=datetime(2026, 9, 8, 18, 0),
        distance_km=4.0,
        duration_minutes=30.0,
        perceived_effort=3,
    )

    second_run = Run(
        datetime=datetime(2026, 9, 10, 18, 30),
        distance_km=5.0,
        duration_minutes=32.0,
        perceived_effort=4,
    )

    service.add_run(first_run)
    service.add_run(second_run)

    runs = service.get_runs()

    assert len(runs) == 2

    assert runs[0].datetime == datetime(
        2026,
        9,
        8,
        18,
        0,
    )
    assert runs[0].distance_km == 4.0

    assert runs[1].datetime == datetime(
        2026,
        9,
        10,
        18,
        30,
    )
    assert runs[1].distance_km == 5.0