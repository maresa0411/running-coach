from running_coach.model.run import Run
from running_coach.model.training_session import TrainingSession
from running_coach.services.llm_service import LLMService


class CoachService:

    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    def generate_feedback(
        self,
        run: Run,
        training_session: TrainingSession,
        previous_runs: list[Run],
    ) -> str:
        prompt = self._build_prompt(
            run=run,
            training_session=training_session,
            previous_runs=previous_runs,
        )

        return self.llm_service.generate(prompt)

    def _build_prompt(
        self,
        run: Run,
        training_session: TrainingSession,
        previous_runs: list[Run],
    ) -> str:
        return f"""
Du bist ein Laufcoach.

Vergleiche den absolvierten Lauf mit der geplanten Trainingseinheit
und gib kurzes, sachliches Feedback.

Geplante Trainingseinheit:
- Woche: {training_session.week}
- Einheit: {training_session.session_number}
- Beschreibung: {training_session.description}
- Zieldauer: {self._format_duration_target(training_session)}
- Zieldistanz: {self._format_distance_target(training_session)}
- Laufintervall: {self._format_minutes(training_session.run_interval_minutes)}
- Gehintervall: {self._format_minutes(training_session.walk_interval_minutes)}
- Zielbelastung: {training_session.target_effort_min}-{training_session.target_effort_max}/10
- Optional: {training_session.optional}

Vorherige Läufe:
{self._format_previous_runs(previous_runs)}

Absolvierter Lauf:
- Distanz: {run.distance_km} km
- Dauer: {run.duration_minutes} Minuten
- Pace: {run.pace_minutes_per_km} min/km
- Subjektive Anstrengung: {run.perceived_effort}/10
- Gehpausen: {run.walk_breaks}
- Laufintervall: {self._format_minutes(run.run_interval_minutes)}
- Gehintervall: {self._format_minutes(run.walk_interval_minutes)}
- Durchschnittspuls: {run.average_heart_rate}
- Maximalpuls: {run.max_heart_rate}

Beurteile insbesondere:
- ob die geplante Dauer oder Distanz ungefähr eingehalten wurde,
- ob die subjektive Belastung zur Zielbelastung passt,
- ob vorhandene Run-Walk-Intervalle eingehalten wurden,
- ob im Vergleich zu den vorherigen Läufen eine Entwicklung erkennbar ist,
- ob die Einheit insgesamt kontrolliert absolviert wurde.

Antworte auf Deutsch in maximal 5 Sätzen.
""".strip()

    def _format_previous_runs(
        self,
        previous_runs: list[Run],
    ) -> str:
        if not previous_runs:
            return "Keine vorherigen Läufe vorhanden."

        recent_runs = previous_runs[-3:]

        lines = []

        for index, previous_run in enumerate(
            recent_runs,
            start=1,
        ):
            lines.append(
                f"{index}. "
                f"{previous_run.distance_km} km, "
                f"{previous_run.duration_minutes} Minuten, "
                f"{previous_run.pace_minutes_per_km} min/km, "
                f"Anstrengung {previous_run.perceived_effort}/10, "
                f"Gehpausen: {previous_run.walk_breaks}"
            )

        return "\n".join(lines)

    def _format_duration_target(
        self,
        training_session: TrainingSession,
    ) -> str:
        minimum = training_session.target_duration_min_minutes
        maximum = training_session.target_duration_max_minutes

        if minimum is None and maximum is None:
            return "nicht vorgegeben"

        if minimum == maximum:
            return f"{minimum} Minuten"

        if minimum is None:
            return f"maximal {maximum} Minuten"

        if maximum is None:
            return f"mindestens {minimum} Minuten"

        return f"{minimum}–{maximum} Minuten"

    def _format_distance_target(
        self,
        training_session: TrainingSession,
    ) -> str:
        minimum = training_session.target_distance_min_km
        maximum = training_session.target_distance_max_km

        if minimum is None and maximum is None:
            return "nicht vorgegeben"

        if minimum == maximum:
            return f"{minimum} km"

        if minimum is None:
            return f"maximal {maximum} km"

        if maximum is None:
            return f"mindestens {minimum} km"

        return f"{minimum}–{maximum} km"

    def _format_minutes(self, value: int | None) -> str:
        if value is None:
            return "nicht vorgegeben"

        if value == 1:
            return "1 Minute"

        return f"{value} Minuten"