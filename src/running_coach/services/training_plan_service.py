import json
from datetime import date, datetime

from running_coach.model.training_session import TrainingSession

from datetime import date
from pathlib import Path


class TrainingPlanService:

    def __init__(
        self,
        training_plan_path: Path,
    ) -> None:
        self.training_plan_path = training_plan_path

        data = self._load_training_plan()

        self.start_date = date.fromisoformat(
            data["start_date"]
        )
        self._number_of_weeks = len(data["weeks"])

        if self.start_date.weekday() != 0:
            raise ValueError(
                "Training plan start date must be a Monday."
            )

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
                    target_duration_min_minutes=session_data[
                        "target_duration_min_minutes"
                    ],
                    target_duration_max_minutes=session_data[
                        "target_duration_max_minutes"
                    ],
                    target_distance_min_km=session_data[
                        "target_distance_min_km"
                    ],
                    target_distance_max_km=session_data[
                        "target_distance_max_km"
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

    def get_week_for_datetime(
            self,
            run_datetime: datetime,
    ) -> int:
        run_date = run_datetime.date()

        days_since_start = (
                run_date - self.start_date
        ).days

        if days_since_start < 0:
            raise ValueError(
                "Run datetime is before training plan start date."
            )

        week = days_since_start // 7 + 1

        if week > self._number_of_weeks:
            raise ValueError(
                "Run datetime is after training plan end date."
            )

        return week

    def _load_training_plan(self) -> dict:
        with self.training_plan_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def get_sessions_for_week(
            self,
            week: int,
    ) -> list[TrainingSession]:
        data = self._load_training_plan()

        for week_data in data["weeks"]:
            if week_data["week"] != week:
                continue

            return [
                TrainingSession(
                    week=week,
                    session_number=session_data[
                        "session_number"
                    ],
                    description=session_data[
                        "description"
                    ],
                    target_duration_min_minutes=session_data[
                        "target_duration_min_minutes"
                    ],
                    target_duration_max_minutes=session_data[
                        "target_duration_max_minutes"
                    ],
                    target_distance_min_km=session_data[
                        "target_distance_min_km"
                    ],
                    target_distance_max_km=session_data[
                        "target_distance_max_km"
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
                    optional=session_data[
                        "optional"
                    ],
                )
                for session_data in week_data["sessions"]
            ]

        raise ValueError(
            f"Training week not found: {week}"
        )