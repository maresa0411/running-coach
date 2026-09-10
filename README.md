# Running Coach

A personal AI-powered running coach built with Python.

The application collects completed runs through Discord, matches them with the current training plan, generates personalized feedback using a local LLM via Ollama, and stores the run history.

## Features

- Interactive run entry via Discord using the `!run` command
- Display the current weekly training plan with `!plan`
- LLM-generated feedback based on the planned training session, current run data, and previous runs

## Configuration

Create a `.env` file in the project root:

```dotenv
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_CHANNEL_ID=your_channel_id
OLLAMA_MODEL=your_locally_running_ollama_model
```

The training plan is configured in:

```text
config/training_plan.json
```

It contains the plan start date and all weekly training sessions like this example shows.

```json
{
  "start_date": "2026-09-07",
  "weeks": [
    {
      "week": 1,
      "sessions": [
        {
          "session_number": 1,
          "description": "30 minutes run-walk",
          "target_duration_min_minutes": 30,
          "target_duration_max_minutes": 30,
          "target_distance_min_km": null,
          "target_distance_max_km": null,
          "run_interval_minutes": 4,
          "walk_interval_minutes": 1,
          "target_effort_min": 3,
          "target_effort_max": 4,
          "optional": false
        }
      ]
    }
  ]
}
```

Instructions for the AI coach are stored in:

```text
config/coach_instructions.md
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

## Run

Start the application:

```bash
python -m running_coach.main
```

Then use the Discord commands:

```text
!run   - Enter a completed run
!plan  - Show the current week's training plan
```

## Tests

Run the tests with:

```bash
pytest
```