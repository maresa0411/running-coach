from dataclasses import dataclass
from datetime import datetime

@dataclass
class Run:
    datetime: datetime
    distance_km: float
    duration_minutes: float
    perceived_effort: int
    walk_breaks: int | None = None
    run_interval_minutes: int | None = None
    walk_interval_minutes: int | None = None
    average_heart_rate: int | None = None
    max_heart_rate: int | None = None


    def __post_init__(self) -> None:
        if not isinstance(self.datetime, datetime):
            raise ValueError(
                "datetime must be a valid datetime object."
            )
        if self.distance_km <= 0:
            raise ValueError("distance_km must be greater than 0.")

        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be greater than 0.")

        if not 1 <= self.perceived_effort <= 10:
            raise ValueError("perceived_effort must be between 1 and 10.")

        if self.walk_breaks is not None and self.walk_breaks < 0:
            raise ValueError("walk_breaks cannot be negative.")

        if self.average_heart_rate is not None and self.average_heart_rate <= 0:
            raise ValueError("average_heart_rate cannot be negative.")

        if self.max_heart_rate is not None and self.max_heart_rate <= 0:
            raise ValueError("max_heart_freq cannot be negative.")

        if (
                self.average_heart_rate is not None
                and self.max_heart_rate is not None
                and self.average_heart_rate > self.max_heart_rate
        ):
            raise ValueError(
                "average_heart_freq cannot be greater than max_heart_freq."
            )

        has_run_interval = self.run_interval_minutes is not None
        has_walk_interval = self.walk_interval_minutes is not None

        if has_run_interval != has_walk_interval:
            raise ValueError(
                "run_interval_minutes and walk_interval_minutes "
                "must either both be set or both be None."
            )

        if self.run_interval_minutes is not None and self.run_interval_minutes <= 0:
            raise ValueError(
                "run_interval_minutes must be greater than 0."
            )

        if self.walk_interval_minutes is not None and self.walk_interval_minutes <= 0:
            raise ValueError(
                "walk_interval_minutes must be greater than 0."
            )


    @property
    def pace_minutes_per_km(self) -> float:
        return round(self.duration_minutes / self.distance_km, 2)