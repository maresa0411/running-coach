import json
from pathlib import Path

from running_coach.model.run import Run


class RunHistoryService:

    def __init__(self, runs_path: Path) -> None:
        self.runs_path = runs_path

    def get_runs(self) -> list[Run]:
        if not self.runs_path.exists():
            return []

        with self.runs_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        return [
            Run(
                distance_km=run_data["distance_km"],
                duration_minutes=run_data["duration_minutes"],
                perceived_effort=run_data["perceived_effort"],
                walk_breaks=run_data["walk_breaks"],
                run_interval_minutes=run_data["run_interval_minutes"],
                walk_interval_minutes=run_data["walk_interval_minutes"],
                average_heart_rate=run_data["average_heart_rate"],
                max_heart_rate=run_data["max_heart_rate"],
            )
            for run_data in data
        ]

    def add_run(self, run: Run) -> None:
        runs = self.get_runs()
        runs.append(run)

        data = [
            {
                "distance_km": stored_run.distance_km,
                "duration_minutes": stored_run.duration_minutes,
                "perceived_effort": stored_run.perceived_effort,
                "walk_breaks": stored_run.walk_breaks,
                "run_interval_minutes": stored_run.run_interval_minutes,
                "walk_interval_minutes": stored_run.walk_interval_minutes,
                "average_heart_rate": stored_run.average_heart_rate,
                "max_heart_rate": stored_run.max_heart_rate,
            }
            for stored_run in runs
        ]

        self.runs_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.runs_path.open(
            mode="w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False,
            )