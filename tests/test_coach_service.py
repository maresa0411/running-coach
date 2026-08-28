from running_coach.model.run import Run
from running_coach.services.coach_service import CoachService
from running_coach.services.llm_service import LLMService


class FakeOllamaService(LLMService):

    def __init__(self) -> None:
        self.last_prompt: str | None = None

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return "Test feedback"


def test_generate_feedback_returns_llm_response() -> None:
    fake_ollama = FakeOllamaService()
    coach_service = CoachService(llm_service=fake_ollama)

    run = Run(
        distance_km=5.0,
        duration_minutes=42.0,
        perceived_effort=4,
        walk_breaks=8,
        run_interval_minutes=4,
        walk_interval_minutes=1,
    )

    feedback = coach_service.generate_feedback(run)

    assert feedback == "Test feedback"

def test_prompt_contains_run_data() -> None:
    fake_ollama = FakeOllamaService()
    coach_service = CoachService(llm_service=fake_ollama)

    run = Run(
        distance_km=5.0,
        duration_minutes=42.0,
        perceived_effort=4,
        walk_breaks=8,
        run_interval_minutes=4,
        walk_interval_minutes=1,
        average_heart_rate=145,
        max_heart_rate=170,
    )

    coach_service.generate_feedback(run)

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "5.0 km" in prompt
    assert "42.0 Minuten" in prompt
    assert "4/10" in prompt
    assert "8" in prompt
    assert "145" in prompt
    assert "170" in prompt

def test_prompt_contains_run_walk_intervals() -> None:
    fake_ollama = FakeOllamaService()
    coach_service = CoachService(llm_service=fake_ollama)

    run = Run(
        distance_km=5.0,
        duration_minutes=42.0,
        perceived_effort=4,
        walk_breaks=8,
        run_interval_minutes=4,
        walk_interval_minutes=1,
    )

    coach_service.generate_feedback(run)

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "Laufintervall: 4" in prompt
    assert "Gehintervall: 1" in prompt