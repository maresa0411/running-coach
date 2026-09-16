import pytest

from running_coach.services.running_coach_workflow import (
    CompletedRunInput,
    RunningCoachWorkflow,
)


USER_ID = 123


def start_until_effort(
    workflow: RunningCoachWorkflow,
) -> None:
    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "5.0")
    workflow.handle_message(USER_ID, "32:00")


def complete_run(
    workflow: RunningCoachWorkflow,
) -> CompletedRunInput:
    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "5.0")
    workflow.handle_message(USER_ID, "32:00")
    workflow.handle_message(USER_ID, "4")
    workflow.handle_message(USER_ID, "6")
    workflow.handle_message(USER_ID, "4")
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "145")

    result = workflow.handle_message(USER_ID, "162")

    assert isinstance(result, CompletedRunInput)

    return result


def test_start_asks_for_session() -> None:
    workflow = RunningCoachWorkflow()

    response = workflow.start(USER_ID)

    assert "Welche Einheit war das?" in response


def test_invalid_session_is_rejected() -> None:
    workflow = RunningCoachWorkflow()
    workflow.start(USER_ID)

    response = workflow.handle_message(
        USER_ID,
        "4",
    )

    assert response == "Bitte antworte mit 1, 2 oder 3."


def test_valid_session_asks_for_distance() -> None:
    workflow = RunningCoachWorkflow()
    workflow.start(USER_ID)

    response = workflow.handle_message(
        USER_ID,
        "1",
    )

    assert response == (
        "Wie weit bist du gelaufen? Bitte in km angeben."
    )


def test_distance_accepts_comma() -> None:
    workflow = RunningCoachWorkflow()
    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")

    response = workflow.handle_message(
        USER_ID,
        "5,2",
    )

    assert response == (
        "Wie lange hat der Lauf gedauert? Bitte im Format Minuten:Sekunden."
    )

    assert workflow.run_data[USER_ID]["distance_km"] == 5.2


def test_invalid_distance_is_rejected() -> None:
    workflow = RunningCoachWorkflow()
    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")

    response = workflow.handle_message(
        USER_ID,
        "abc",
    )

    assert response == (
        "Bitte gib die Distanz als Zahl an, z. B. 5.2."
    )


def test_zero_distance_is_rejected() -> None:
    workflow = RunningCoachWorkflow()
    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")

    response = workflow.handle_message(
        USER_ID,
        "0",
    )

    assert response == (
        "Die Distanz muss größer als 0 sein."
    )


def test_duration_accepts_minutes_and_seconds() -> None:
    workflow = RunningCoachWorkflow()

    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "5.0")

    response = workflow.handle_message(
        USER_ID,
        "34:28",
    )

    assert response == (
        "Wie anstrengend war der Lauf von 1–10?"
    )

    assert workflow.run_data[USER_ID][
        "duration_minutes"
    ] == pytest.approx(
        34 + 28 / 60
    )


def test_duration_accepts_zero_seconds() -> None:
    workflow = RunningCoachWorkflow()

    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "5.0")

    workflow.handle_message(
        USER_ID,
        "32:00",
    )

    assert workflow.run_data[USER_ID][
        "duration_minutes"
    ] == 32.0


def test_invalid_duration_format_is_rejected() -> None:
    workflow = RunningCoachWorkflow()

    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "5.0")

    response = workflow.handle_message(
        USER_ID,
        "32",
    )

    assert response == (
        "Bitte gib die Dauer im Format Minuten:Sekunden an."
    )


def test_invalid_duration_seconds_are_rejected() -> None:
    workflow = RunningCoachWorkflow()

    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "5.0")

    response = workflow.handle_message(
        USER_ID,
        "32:60",
    )

    assert response == (
        "Bitte gib eine gültige Dauer im Format "
        "Minuten:Sekunden an."
    )


def test_zero_duration_is_rejected() -> None:
    workflow = RunningCoachWorkflow()

    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "5.0")

    response = workflow.handle_message(
        USER_ID,
        "0:00",
    )

    assert response == (
        "Die Dauer muss größer als 0 sein."
    )


def test_invalid_effort_is_rejected() -> None:
    workflow = RunningCoachWorkflow()

    start_until_effort(workflow)

    response = workflow.handle_message(
        USER_ID,
        "11",
    )

    assert response == (
        "Bitte gib eine Zahl von 1 bis 10 ein."
    )


def test_negative_walk_breaks_are_rejected() -> None:
    workflow = RunningCoachWorkflow()

    start_until_effort(workflow)
    workflow.handle_message(USER_ID, "4")

    response = workflow.handle_message(
        USER_ID,
        "-2",
    )

    assert response == (
        "Die Anzahl der Gehpausen darf nicht negativ sein."
    )


def test_optional_walk_breaks_accept_dash() -> None:
    workflow = RunningCoachWorkflow()

    start_until_effort(workflow)
    workflow.handle_message(USER_ID, "4")

    response = workflow.handle_message(
        USER_ID,
        "-",
    )

    assert "Laufintervalle" in response
    assert workflow.run_data[USER_ID]["walk_breaks"] is None


def test_run_and_walk_intervals_must_both_be_set() -> None:
    workflow = RunningCoachWorkflow()

    start_until_effort(workflow)
    workflow.handle_message(USER_ID, "4")
    workflow.handle_message(USER_ID, "6")
    workflow.handle_message(USER_ID, "4")

    response = workflow.handle_message(
        USER_ID,
        "-",
    )

    assert response == (
        "Lauf- und Gehintervall müssen entweder beide "
        "angegeben oder beide mit - übersprungen werden."
    )


def test_average_heart_rate_must_not_exceed_max() -> None:
    workflow = RunningCoachWorkflow()

    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "5")
    workflow.handle_message(USER_ID, "32:00")
    workflow.handle_message(USER_ID, "4")
    workflow.handle_message(USER_ID, "6")
    workflow.handle_message(USER_ID, "4")
    workflow.handle_message(USER_ID, "1")
    workflow.handle_message(USER_ID, "170")

    response = workflow.handle_message(
        USER_ID,
        "160",
    )

    assert response == (
        "Die durchschnittliche Herzfrequenz darf nicht "
        "höher als die maximale Herzfrequenz sein."
    )


def test_completed_workflow_returns_run() -> None:
    workflow = RunningCoachWorkflow()

    result = complete_run(workflow)

    assert result.session_number == 1

    assert result.run.distance_km == 5.0
    assert result.run.duration_minutes == 32.0
    assert result.run.perceived_effort == 4
    assert result.run.walk_breaks == 6
    assert result.run.run_interval_minutes == 4
    assert result.run.walk_interval_minutes == 1
    assert result.run.average_heart_rate == 145
    assert result.run.max_heart_rate == 162


def test_completed_workflow_clears_state() -> None:
    workflow = RunningCoachWorkflow()

    complete_run(workflow)

    assert USER_ID not in workflow.states
    assert USER_ID not in workflow.session_numbers
    assert USER_ID not in workflow.run_data


def test_optional_fields_can_all_be_none() -> None:
    workflow = RunningCoachWorkflow()

    workflow.start(USER_ID)
    workflow.handle_message(USER_ID, "2")
    workflow.handle_message(USER_ID, "5")
    workflow.handle_message(USER_ID, "35:00")
    workflow.handle_message(USER_ID, "3")
    workflow.handle_message(USER_ID, "-")
    workflow.handle_message(USER_ID, "-")
    workflow.handle_message(USER_ID, "-")
    workflow.handle_message(USER_ID, "-")

    result = workflow.handle_message(
        USER_ID,
        "-",
    )

    assert isinstance(result, CompletedRunInput)

    assert result.session_number == 2
    assert result.run.walk_breaks is None
    assert result.run.run_interval_minutes is None
    assert result.run.walk_interval_minutes is None
    assert result.run.average_heart_rate is None
    assert result.run.max_heart_rate is None


def test_message_without_active_dialog_is_rejected() -> None:
    workflow = RunningCoachWorkflow()

    response = workflow.handle_message(
        USER_ID,
        "5",
    )

    assert response == (
        "Kein aktiver Dialog. Starte mit !run."
    )