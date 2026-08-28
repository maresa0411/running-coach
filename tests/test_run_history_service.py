import json

from running_coach.model.run import Run
from running_coach.services.run_history_service import RunHistoryService


def test_get_runs_returns_empty_list_when_file_does_not_exist(
    tmp_path,
) -> None:
    runs_path = tmp_path / "runs.json"

    service = RunHistoryService(
        runs_path=runs_path
    )

    runs = service.get_runs()

    assert runs == []


def test_add_run_saves_run(
    tmp_path,
) -> None:
    runs_path = tmp_path / "runs.json"

    service = RunHistoryService(
        runs_path=runs_path
    )

    run = Run(
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
        walk_breaks=3,
        run_interval_minutes=4,
        walk_interval_minutes=1,
        average_heart_rate=145,
        max_heart_rate=170,
    )

    service.add_run(run)

    assert runs_path.exists()

    data = json.loads(
        runs_path.read_text(
            encoding="utf-8"
        )
    )

    assert len(data) == 1
    assert data[0]["distance_km"] == 5.0
    assert data[0]["duration_minutes"] == 40.0
    assert data[0]["perceived_effort"] == 4
    assert data[0]["walk_breaks"] == 3
    assert data[0]["run_interval_minutes"] == 4
    assert data[0]["walk_interval_minutes"] == 1
    assert data[0]["average_heart_rate"] == 145
    assert data[0]["max_heart_rate"] == 170


def test_get_runs_loads_saved_runs(
    tmp_path,
) -> None:
    runs_path = tmp_path / "runs.json"

    service = RunHistoryService(
        runs_path=runs_path
    )

    run = Run(
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
        walk_breaks=3,
        run_interval_minutes=4,
        walk_interval_minutes=1,
        average_heart_rate=145,
        max_heart_rate=170,
    )

    service.add_run(run)

    runs = service.get_runs()

    assert len(runs) == 1

    loaded_run = runs[0]

    assert loaded_run.distance_km == 5.0
    assert loaded_run.duration_minutes == 40.0
    assert loaded_run.perceived_effort == 4
    assert loaded_run.walk_breaks == 3
    assert loaded_run.run_interval_minutes == 4
    assert loaded_run.walk_interval_minutes == 1
    assert loaded_run.average_heart_rate == 145
    assert loaded_run.max_heart_rate == 170


def test_add_run_keeps_existing_runs(
    tmp_path,
) -> None:
    runs_path = tmp_path / "runs.json"

    service = RunHistoryService(
        runs_path=runs_path
    )

    first_run = Run(
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    second_run = Run(
        distance_km=5.5,
        duration_minutes=42.0,
        perceived_effort=3,
    )

    service.add_run(first_run)
    service.add_run(second_run)

    runs = service.get_runs()

    assert len(runs) == 2

    assert runs[0].distance_km == 5.0
    assert runs[1].distance_km == 5.5