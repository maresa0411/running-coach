from running_coach.model.run import Run
from running_coach.services.llm_service import LLMService


class CoachService:

    def __init__(self, llm_service: LLMService) -> None:
        self.llm_service = llm_service

    def generate_feedback(self, run: Run) -> str:
        prompt = self._build_prompt(run)
        return self.llm_service.generate(prompt)

    def _build_prompt(self, run: Run) -> str:
        return f"""
Du bist ein Laufcoach.

Bewerte den folgenden Lauf kurz und sachlich.

Laufdaten:
- Distanz: {run.distance_km} km
- Dauer: {run.duration_minutes} Minuten
- Pace: {run.pace_minutes_per_km} min/km
- Subjektive Anstrengung: {run.perceived_effort}/10
- Gehpausen: {run.walk_breaks}
- Laufintervall: {run.run_interval_minutes}
- Gehintervall: {run.walk_interval_minutes}
- Durchschnittspuls: {run.average_heart_rate}
- Maximalpuls: {run.max_heart_rate}

Das Ziel ist momentan, lockere Läufe kontrolliert und mit niedriger Belastung zu absolvieren.

Antworte auf Deutsch in maximal 5 Sätzen.
""".strip()