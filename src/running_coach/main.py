import asyncio
import os
from pathlib import Path

import discord
from dotenv import load_dotenv
from datetime import date

from running_coach.services.coach_service import CoachService
from running_coach.services.discord_service import DiscordService
from running_coach.services.ollama_service import OllamaService
from running_coach.services.run_history_service import RunHistoryService
from running_coach.services.running_coach_workflow import (
    CompletedRunInput,
    RunningCoachWorkflow,
)
from running_coach.services.training_plan_service import TrainingPlanService

async def main() -> None:
    load_dotenv()

    project_root = Path(__file__).resolve().parents[2]

    training_plan_service = TrainingPlanService(
        training_plan_path=project_root
        / "config"
        / "training_plan.json"
    )

    run_history_service = RunHistoryService(
        runs_path=project_root
        / "data"
        / "runs.json"
    )

    ollama_service = OllamaService(
        model="gemma4:latest"
    )

    coach_service = CoachService(
        llm_service=ollama_service
    )

    workflow = RunningCoachWorkflow()

    token = os.getenv("DISCORD_BOT_TOKEN")
    channel_id = os.getenv("DISCORD_CHANNEL_ID")

    if token is None:
        raise ValueError("DISCORD_BOT_TOKEN is not set")

    if channel_id is None:
        raise ValueError("DISCORD_CHANNEL_ID is not set")

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    discord_service = DiscordService(client=client)

    @client.event
    async def on_ready() -> None:
        print(f"Eingeloggt als {client.user}")

    @client.event
    async def on_message(
        message: discord.Message,
    ) -> None:
        if message.author.bot:
            return

        if str(message.channel.id) != channel_id:
            return

        user_id = message.author.id
        content = message.content.strip()

        if content == "!run":
            response = workflow.start(user_id)

            await discord_service.send_message(recipient=channel_id, message=response)
            return

        result = workflow.handle_message(
            user_id=user_id,
            message=content,
        )

        if isinstance(result, str):
            await discord_service.send_message(recipient=channel_id, message=result)
            return

        if isinstance(result, CompletedRunInput):
            run = result.run
            session_number = result.session_number

            week = training_plan_service.get_week_for_datetime(
                run.datetime
            )

            training_session = training_plan_service.get_session(
                week=week,
                session_number=session_number,
            )

            previous_runs = run_history_service.get_runs()

            await discord_service.send_message(recipient=channel_id, message="Lauf vollständig erfasst. "
                "Ich erstelle dein Feedback...")

            feedback = await asyncio.to_thread(
                coach_service.generate_feedback,
                run,
                training_session,
                previous_runs,
            )

            await discord_service.send_message(recipient=channel_id, message=feedback)

            run_history_service.add_run(run)

    await client.start(token)


if __name__ == "__main__":
    asyncio.run(main())