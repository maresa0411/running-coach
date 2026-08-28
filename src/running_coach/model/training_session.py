from dataclasses import dataclass


@dataclass
class TrainingSession:
    week: int
    session_number: int
    description: str

    target_duration_min_minutes: int | None = None
    target_duration_max_minutes: int | None = None

    target_distance_min_km: float | None = None
    target_distance_max_km: float | None = None

    run_interval_minutes: int | None = None
    walk_interval_minutes: int | None = None

    target_effort_min: int | None = None
    target_effort_max: int | None = None

    optional: bool = False

    def __post_init__(self) -> None:
        if self.week < 1:
            raise ValueError("week must be greater than 0.")

        if self.session_number < 1:
            raise ValueError("session_number must be greater than 0.")

        if not self.description.strip():
            raise ValueError("description cannot be empty.")

        if (
                self.target_duration_min_minutes is not None
                and self.target_duration_min_minutes <= 0
        ):
            raise ValueError(
                "target_duration_min_minutes must be greater than 0."
            )

        if (
                self.target_duration_max_minutes is not None
                and self.target_duration_max_minutes <= 0
        ):
            raise ValueError(
                "target_duration_max_minutes must be greater than 0."
            )

        if (
                self.target_duration_min_minutes is not None
                and self.target_duration_max_minutes is not None
                and self.target_duration_min_minutes > self.target_duration_max_minutes
        ):
            raise ValueError(
                "target_duration_min_minutes cannot be greater than "
                "target_duration_max_minutes."
            )

        if (
                self.target_distance_min_km is not None
                and self.target_distance_min_km <= 0
        ):
            raise ValueError(
                "target_distance_min_km must be greater than 0."
            )

        if (
                self.target_distance_max_km is not None
                and self.target_distance_max_km <= 0
        ):
            raise ValueError(
                "target_distance_max_km must be greater than 0."
            )

        if (
                self.target_distance_min_km is not None
                and self.target_distance_max_km is not None
                and self.target_distance_min_km > self.target_distance_max_km
        ):
            raise ValueError(
                "target_distance_min_km cannot be greater than "
                "target_distance_max_km."
            )

        has_run_interval = self.run_interval_minutes is not None
        has_walk_interval = self.walk_interval_minutes is not None

        if has_run_interval != has_walk_interval:
            raise ValueError(
                "run_interval_minutes and walk_interval_minutes "
                "must either both be set or both be None."
            )

        if (
                self.run_interval_minutes is not None
                and self.run_interval_minutes <= 0
        ):
            raise ValueError(
                "run_interval_minutes must be greater than 0."
            )

        if (
                self.walk_interval_minutes is not None
                and self.walk_interval_minutes <= 0
        ):
            raise ValueError(
                "walk_interval_minutes must be greater than 0."
            )

        has_effort_min = self.target_effort_min is not None
        has_effort_max = self.target_effort_max is not None

        if has_effort_min != has_effort_max:
            raise ValueError(
                "target_effort_min and target_effort_max "
                "must either both be set or both be None."
            )

        if (
                self.target_effort_min is not None
                and not 1 <= self.target_effort_min <= 10
        ):
            raise ValueError(
                "target_effort_min must be between 1 and 10."
            )

        if (
                self.target_effort_max is not None
                and not 1 <= self.target_effort_max <= 10
        ):
            raise ValueError(
                "target_effort_max must be between 1 and 10."
            )

        if (
                self.target_effort_min is not None
                and self.target_effort_max is not None
                and self.target_effort_min > self.target_effort_max
        ):
            raise ValueError(
                "target_effort_min cannot be greater than target_effort_max."
            )