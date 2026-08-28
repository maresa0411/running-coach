from running_coach.model.run import Run
from running_coach.services.coach_service import CoachService
from running_coach.services.ollama_service import OllamaService


def main() -> None:
    run = Run(
        distance_km=5.0,
        duration_minutes=42.0,
        perceived_effort=4,
        walk_breaks=8,
        run_interval_minutes=4,
        walk_interval_minutes=1,
    )

    ollama_service = OllamaService(
        model="gemma4:latest"
    )

    coach_service = CoachService(
        ollama_service=ollama_service
    )

    feedback = coach_service.generate_feedback(run)

    print(feedback)


if __name__ == "__main__":
    main()