from running_coach.model.run import Run
from running_coach.model.training_session import TrainingSession
from running_coach.services.coach_service import CoachService
from running_coach.services.llm_service import LLMService


class FakeOllamaService(LLMService):

    def __init__(self) -> None:
        self.last_prompt: str | None = None

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return "Test feedback"


def create_training_session() -> TrainingSession:
    return TrainingSession(
        week=1,
        session_number=1,
        description="Lockerer Run-Walk-Lauf",
        target_duration_min_minutes=30,
        target_duration_max_minutes=35,
        run_interval_minutes=4,
        walk_interval_minutes=1,
        target_effort_min=3,
        target_effort_max=4,
    )


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

    training_session = create_training_session()

    feedback = coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

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

    training_session = create_training_session()

    coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "5.0 km" in prompt
    assert "42.0 Minuten" in prompt
    assert "4/10" in prompt
    assert "Gehpausen: 8" in prompt
    assert "Durchschnittspuls: 145" in prompt
    assert "Maximalpuls: 170" in prompt


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

    training_session = create_training_session()

    coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "Laufintervall: 4 Minuten" in prompt
    assert "Gehintervall: 1 Minute" in prompt


def test_prompt_contains_training_session_data() -> None:
    fake_ollama = FakeOllamaService()
    coach_service = CoachService(llm_service=fake_ollama)

    run = Run(
        distance_km=5.0,
        duration_minutes=30.0,
        perceived_effort=4,
    )

    training_session = create_training_session()

    coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "Woche: 1" in prompt
    assert "Einheit: 1" in prompt
    assert "Lockerer Run-Walk-Lauf" in prompt
    assert "Zieldauer: 30–35 Minuten" in prompt
    assert "Zieldistanz: nicht vorgegeben" in prompt
    assert "Zielbelastung: 3-4/10" in prompt


def test_prompt_formats_exact_duration_target() -> None:
    fake_ollama = FakeOllamaService()
    coach_service = CoachService(llm_service=fake_ollama)

    training_session = TrainingSession(
        week=1,
        session_number=1,
        description="30 Minuten locker",
        target_duration_min_minutes=30,
        target_duration_max_minutes=30,
    )

    run = Run(
        distance_km=5.0,
        duration_minutes=30.0,
        perceived_effort=4,
    )

    coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "Zieldauer: 30 Minuten" in prompt


def test_prompt_formats_minimum_duration_target() -> None:
    fake_ollama = FakeOllamaService()
    coach_service = CoachService(llm_service=fake_ollama)

    training_session = TrainingSession(
        week=1,
        session_number=1,
        description="Mindestens 30 Minuten",
        target_duration_min_minutes=30,
    )

    run = Run(
        distance_km=5.0,
        duration_minutes=30.0,
        perceived_effort=4,
    )

    coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "Zieldauer: mindestens 30 Minuten" in prompt


def test_prompt_formats_maximum_duration_target() -> None:
    fake_ollama = FakeOllamaService()
    coach_service = CoachService(llm_service=fake_ollama)

    training_session = TrainingSession(
        week=1,
        session_number=1,
        description="Maximal 30 Minuten",
        target_duration_max_minutes=30,
    )

    run = Run(
        distance_km=5.0,
        duration_minutes=30.0,
        perceived_effort=4,
    )

    coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "Zieldauer: maximal 30 Minuten" in prompt


def test_prompt_formats_distance_range() -> None:
    fake_ollama = FakeOllamaService()
    coach_service = CoachService(llm_service=fake_ollama)

    training_session = TrainingSession(
        week=2,
        session_number=2,
        description="5–5,5 km locker",
        target_distance_min_km=5.0,
        target_distance_max_km=5.5,
    )

    run = Run(
        distance_km=5.2,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "Zieldistanz: 5.0–5.5 km" in prompt


def test_prompt_formats_exact_distance_target() -> None:
    fake_ollama = FakeOllamaService()
    coach_service = CoachService(llm_service=fake_ollama)

    training_session = TrainingSession(
        week=1,
        session_number=2,
        description="5 km locker",
        target_distance_min_km=5.0,
        target_distance_max_km=5.0,
    )

    run = Run(
        distance_km=5.0,
        duration_minutes=40.0,
        perceived_effort=4,
    )

    coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

    prompt = fake_ollama.last_prompt

    assert prompt is not None
    assert "Zieldistanz: 5.0 km" in prompt