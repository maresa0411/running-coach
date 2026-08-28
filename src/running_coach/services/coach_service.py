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
    ) -> str:
        prompt = self._build_prompt(
            run=run,
            training_session=training_session,
        )

        return self.llm_service.generate(prompt)

    def _build_prompt(
        self,
        run: Run,
        training_session: TrainingSession,
    ) -> str:
        return f"""
Du bist ein Laufcoach.

Vergleiche den absolvierten Lauf mit der geplanten Trainingseinheit
und gib kurzes, sachliches Feedback.

Geplante Trainingseinheit:
- Woche: {training_session.week}
- Einheit: {training_session.session_number}
- Beschreibung: {training_session.description}
- Zieldauer: {training_session.target_duration_minutes} Minuten
- Zieldistanz: {training_session.target_distance_km} km
- Laufintervall: {training_session.run_interval_minutes} Minuten
- Gehintervall: {training_session.walk_interval_minutes} Minuten
- Zielbelastung: {training_session.target_effort_min}-{training_session.target_effort_max}/10
- Optional: {training_session.optional}

Absolvierter Lauf:
- Distanz: {run.distance_km} km
- Dauer: {run.duration_minutes} Minuten
- Pace: {run.pace_minutes_per_km} min/km
- Subjektive Anstrengung: {run.perceived_effort}/10
- Gehpausen: {run.walk_breaks}
- Laufintervall: {run.run_interval_minutes} Minuten
- Gehintervall: {run.walk_interval_minutes} Minuten
- Durchschnittspuls: {run.average_heart_rate}
- Maximalpuls: {run.max_heart_rate}

Beurteile insbesondere:
- ob die geplante Dauer oder Distanz ungefähr eingehalten wurde,
- ob die subjektive Belastung zur Zielbelastung passt,
- ob vorhandene Run-Walk-Intervalle eingehalten wurden,
- ob die Einheit insgesamt kontrolliert absolviert wurde.

Antworte auf Deutsch in maximal 5 Sätzen.
""".strip()