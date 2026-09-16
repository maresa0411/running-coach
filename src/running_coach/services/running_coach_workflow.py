# src/running_coach/services/running_coach_workflow.py

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from running_coach.model.run import Run


class ConversationState(Enum):
    WAITING_FOR_SESSION = "waiting_for_session"
    WAITING_FOR_DISTANCE = "waiting_for_distance"
    WAITING_FOR_DURATION = "waiting_for_duration"
    WAITING_FOR_EFFORT = "waiting_for_effort"
    WAITING_FOR_WALK_BREAKS = "waiting_for_walk_breaks"
    WAITING_FOR_RUN_INTERVAL = "waiting_for_run_interval"
    WAITING_FOR_WALK_INTERVAL = "waiting_for_walk_interval"
    WAITING_FOR_AVERAGE_HEART_RATE = "waiting_for_average_heart_rate"
    WAITING_FOR_MAX_HEART_RATE = "waiting_for_max_heart_rate"


@dataclass
class CompletedRunInput:
    session_number: int
    run: Run


class RunningCoachWorkflow:

    def __init__(self) -> None:
        self.states: dict[int, ConversationState] = {}
        self.session_numbers: dict[int, int] = {}
        self.run_data: dict[int, dict] = {}

    def start(self, user_id: int) -> str:
        self.states[user_id] = ConversationState.WAITING_FOR_SESSION
        self.run_data[user_id] = {}

        return (
            "Welche Einheit war das?\n"
            "1 = Einheit 1\n"
            "2 = Einheit 2\n"
            "3 = Bonus"
        )

    def handle_message(
        self,
        user_id: int,
        message: str,
    ) -> str | CompletedRunInput:
        state = self.states.get(user_id)

        if state is None:
            return "Kein aktiver Dialog. Starte mit !run."

        if state == ConversationState.WAITING_FOR_SESSION:
            return self._handle_session(user_id, message)

        if state == ConversationState.WAITING_FOR_DISTANCE:
            return self._handle_distance(user_id, message)

        if state == ConversationState.WAITING_FOR_DURATION:
            return self._handle_duration(user_id, message)

        if state == ConversationState.WAITING_FOR_EFFORT:
            return self._handle_effort(user_id, message)

        if state == ConversationState.WAITING_FOR_WALK_BREAKS:
            return self._handle_walk_breaks(user_id, message)

        if state == ConversationState.WAITING_FOR_RUN_INTERVAL:
            return self._handle_run_interval(user_id, message)

        if state == ConversationState.WAITING_FOR_WALK_INTERVAL:
            return self._handle_walk_interval(user_id, message)

        if state == ConversationState.WAITING_FOR_AVERAGE_HEART_RATE:
            return self._handle_average_heart_rate(user_id, message)

        if state == ConversationState.WAITING_FOR_MAX_HEART_RATE:
            return self._handle_max_heart_rate(user_id, message)

        return "Unbekannter Dialogzustand."

    def _handle_session(
        self,
        user_id: int,
        message: str,
    ) -> str:
        if message not in {"1", "2", "3"}:
            return "Bitte antworte mit 1, 2 oder 3."

        self.session_numbers[user_id] = int(message)
        self.states[user_id] = ConversationState.WAITING_FOR_DISTANCE

        return "Wie weit bist du gelaufen? Bitte in km angeben."

    def _handle_distance(
        self,
        user_id: int,
        message: str,
    ) -> str:
        try:
            distance = float(message.replace(",", "."))
        except ValueError:
            return "Bitte gib die Distanz als Zahl an, z. B. 5.2."

        if distance <= 0:
            return "Die Distanz muss größer als 0 sein."

        self.run_data[user_id]["distance_km"] = distance
        self.states[user_id] = ConversationState.WAITING_FOR_DURATION

        return "Wie lange hat der Lauf gedauert? Bitte im Format Minuten:Sekunden."

    def _handle_duration(
            self,
            user_id: int,
            message: str,
    ) -> str:
        try:
            minutes_text, seconds_text = message.split(":")
            minutes = int(minutes_text)
            seconds = int(seconds_text)
        except ValueError:
            return "Bitte gib die Dauer im Format Minuten:Sekunden an."

        if minutes < 0 or not 0 <= seconds <= 59:
            return "Bitte gib eine gültige Dauer im Format Minuten:Sekunden an."

        duration = minutes + seconds / 60

        if duration <= 0:
            return "Die Dauer muss größer als 0 sein."

        self.run_data[user_id]["duration_minutes"] = duration
        self.states[user_id] = ConversationState.WAITING_FOR_EFFORT

        return "Wie anstrengend war der Lauf von 1–10?"

    def _handle_effort(
        self,
        user_id: int,
        message: str,
    ) -> str:
        try:
            effort = int(message)
        except ValueError:
            return "Bitte gib eine Zahl von 1 bis 10 ein."

        if not 1 <= effort <= 10:
            return "Bitte gib eine Zahl von 1 bis 10 ein."

        self.run_data[user_id]["perceived_effort"] = effort
        self.states[user_id] = ConversationState.WAITING_FOR_WALK_BREAKS

        return (
            "Wie viele Gehpausen hattest du?\n"
            "Falls unbekannt: -"
        )

    def _handle_walk_breaks(
        self,
        user_id: int,
        message: str,
    ) -> str:
        try:
            walk_breaks = self._parse_optional_int(message)
        except ValueError:
            return "Bitte gib eine Zahl oder - ein."

        if walk_breaks is not None and walk_breaks < 0:
            return "Die Anzahl der Gehpausen darf nicht negativ sein."

        self.run_data[user_id]["walk_breaks"] = walk_breaks
        self.states[user_id] = ConversationState.WAITING_FOR_RUN_INTERVAL

        return (
            "Wie lang waren deine Laufintervalle in Minuten?\n"
            "Falls nicht bekannt oder keine Intervalle: -"
        )

    def _handle_run_interval(
        self,
        user_id: int,
        message: str,
    ) -> str:
        try:
            run_interval = self._parse_optional_int(message)
        except ValueError:
            return "Bitte gib eine Zahl oder - ein."

        if run_interval is not None and run_interval <= 0:
            return "Das Laufintervall muss größer als 0 sein."

        self.run_data[user_id]["run_interval_minutes"] = run_interval
        self.states[user_id] = ConversationState.WAITING_FOR_WALK_INTERVAL

        return (
            "Wie lang waren deine Gehintervalle in Minuten?\n"
            "Falls nicht bekannt oder keine Intervalle: -"
        )

    def _handle_walk_interval(
        self,
        user_id: int,
        message: str,
    ) -> str:
        try:
            walk_interval = self._parse_optional_int(message)
        except ValueError:
            return "Bitte gib eine Zahl oder - ein."

        if walk_interval is not None and walk_interval <= 0:
            return "Das Gehintervall muss größer als 0 sein."

        run_interval = self.run_data[user_id]["run_interval_minutes"]

        if (run_interval is None) != (walk_interval is None):
            return (
                "Lauf- und Gehintervall müssen entweder beide "
                "angegeben oder beide mit - übersprungen werden."
            )

        self.run_data[user_id]["walk_interval_minutes"] = walk_interval
        self.states[user_id] = (
            ConversationState.WAITING_FOR_AVERAGE_HEART_RATE
        )

        return (
            "Wie hoch war deine durchschnittliche Herzfrequenz?\n"
            "Falls unbekannt: -"
        )

    def _handle_average_heart_rate(
        self,
        user_id: int,
        message: str,
    ) -> str:
        try:
            average_heart_rate = self._parse_optional_int(message)
        except ValueError:
            return "Bitte gib eine Zahl oder - ein."

        if (
            average_heart_rate is not None
            and average_heart_rate <= 0
        ):
            return "Die Herzfrequenz muss größer als 0 sein."

        self.run_data[user_id][
            "average_heart_rate"
        ] = average_heart_rate

        self.states[user_id] = (
            ConversationState.WAITING_FOR_MAX_HEART_RATE
        )

        return (
            "Wie hoch war deine maximale Herzfrequenz?\n"
            "Falls unbekannt: -"
        )

    def _handle_max_heart_rate(
        self,
        user_id: int,
        message: str,
    ) -> str | CompletedRunInput:
        try:
            max_heart_rate = self._parse_optional_int(message)
        except ValueError:
            return "Bitte gib eine Zahl oder - ein."

        if max_heart_rate is not None and max_heart_rate <= 0:
            return "Die Herzfrequenz muss größer als 0 sein."

        average_heart_rate = self.run_data[user_id][
            "average_heart_rate"
        ]

        if (
            average_heart_rate is not None
            and max_heart_rate is not None
            and average_heart_rate > max_heart_rate
        ):
            return (
                "Die durchschnittliche Herzfrequenz darf nicht "
                "höher als die maximale Herzfrequenz sein."
            )

        self.run_data[user_id]["max_heart_rate"] = max_heart_rate

        data = self.run_data[user_id]

        try:
            run = Run(
                datetime=datetime.now(),
                distance_km=data["distance_km"],
                duration_minutes=data["duration_minutes"],
                perceived_effort=data["perceived_effort"],
                walk_breaks=data["walk_breaks"],
                run_interval_minutes=data["run_interval_minutes"],
                walk_interval_minutes=data["walk_interval_minutes"],
                average_heart_rate=data["average_heart_rate"],
                max_heart_rate=data["max_heart_rate"],
            )
        except ValueError as error:
            return f"Die Laufdaten sind ungültig: {error}"

        result = CompletedRunInput(
            session_number=self.session_numbers[user_id],
            run=run,
        )

        self._clear_user(user_id)

        return result

    def _parse_optional_int(
        self,
        message: str,
    ) -> int | None:
        value = message.strip()

        if value == "-":
            return None

        return int(value)

    def _clear_user(
        self,
        user_id: int,
    ) -> None:
        self.states.pop(user_id, None)
        self.session_numbers.pop(user_id, None)
        self.run_data.pop(user_id, None)