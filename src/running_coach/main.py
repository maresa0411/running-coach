from pathlib import Path

from running_coach.services.training_plan_service import TrainingPlanService
from running_coach.model.run import Run
from running_coach.services.coach_service import CoachService
from running_coach.services.ollama_service import OllamaService


def main() -> None:
    run = Run(
        distance_km=5.0,
        duration_minutes=32.0,
        perceived_effort=4,
        walk_breaks=6,
        run_interval_minutes=4,
        walk_interval_minutes=1,
    )

    project_root = Path(__file__).resolve().parents[2]

    training_plan_service = TrainingPlanService(
        training_plan_path=project_root / "config" / "training_plan.json"
    )

    training_session = training_plan_service.get_session(
        week=1,
        session_number=1,
    )

    ollama_service = OllamaService(
        model="gemma4:latest"
    )

    coach_service = CoachService(
        llm_service=ollama_service
    )

    feedback = coach_service.generate_feedback(
        run=run,
        training_session=training_session,
    )

    print(feedback)


if __name__ == "__main__":
    main()