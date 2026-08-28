from pathlib import Path

from running_coach.services.run_history_service import RunHistoryService
from running_coach.services.training_plan_service import TrainingPlanService
from running_coach.model.run import Run
from running_coach.services.coach_service import CoachService
from running_coach.services.ollama_service import OllamaService


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]

    run = Run(
        distance_km=5.0,
        duration_minutes=32.0,
        perceived_effort=4,
        walk_breaks=6,
        run_interval_minutes=4,
        walk_interval_minutes=1,
    )

    training_plan_service = TrainingPlanService(
        training_plan_path=project_root / "config" / "training_plan.json"
    )

    training_session = training_plan_service.get_session(
        week=1,
        session_number=1,
    )

    run_history_service = RunHistoryService(
        runs_path=project_root / "data" / "runs.json"
    )

    previous_runs = run_history_service.get_runs()

    print(f"Bisher gespeicherte Läufe: {len(previous_runs)}")

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

    run_history_service.add_run(run)

    print("Lauf wurde gespeichert.")


if __name__ == "__main__":
    main()