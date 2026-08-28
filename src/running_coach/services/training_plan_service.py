import json
from pathlib import Path

from running_coach.model.training_session import TrainingSession


class TrainingPlanService:

    def __init__(self, training_plan_path: Path) -> None:
        self.training_plan_path = training_plan_path

    def get_session(
        self,
        week: int,
        session_number: int,
    ) -> TrainingSession:
        data = self._load_training_plan()

        for week_data in data["weeks"]:
            if week_data["week"] != week:
                continue

            for session_data in week_data["sessions"]:
                if session_data["session_number"] != session_number:
                    continue

                return TrainingSession(
                    week=week,
                    session_number=session_data["session_number"],
                    description=session_data["description"],
                    target_duration_minutes=session_data[
                        "target_duration_minutes"
                    ],
                    target_distance_km=session_data[
                        "target_distance_km"
                    ],
                    run_interval_minutes=session_data[
                        "run_interval_minutes"
                    ],
                    walk_interval_minutes=session_data[
                        "walk_interval_minutes"
                    ],
                    target_effort_min=session_data[
                        "target_effort_min"
                    ],
                    target_effort_max=session_data[
                        "target_effort_max"
                    ],
                    optional=session_data["optional"],
                )

        raise ValueError(
            f"Training session not found: "
            f"week={week}, session_number={session_number}"
        )

    def _load_training_plan(self) -> dict:
        with self.training_plan_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            return json.load(file)