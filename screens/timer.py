import flet as ft
from datetime import datetime, date

from database.db import add_study_session
from services import study_state


def timer_view(page):

    timer_text = ft.Text(
        "00:00:00",
        size=40,
        weight=ft.FontWeight.BOLD
    )

    result_text = ft.Text()

    subject = ft.Dropdown(
        width=250,
        options=[
            ft.dropdown.Option("Quant"),
            ft.dropdown.Option("Reasoning"),
            ft.dropdown.Option("English"),
            ft.dropdown.Option("GA"),
        ]
    )

    topic = ft.TextField(
        label="Topic",
        width=300
    )

    if study_state.running:
        subject.value = study_state.current_subject
        topic.value = study_state.current_topic

        elapsed = datetime.now() - study_state.start_time

        total_seconds = int(elapsed.total_seconds())

        hrs = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        timer_text.value = f"{hrs:02}:{mins:02}:{secs:02}"

    def start_study(e):

        if study_state.running:
            result_text.value = "Session already running"
            page.update()
            return

        if not subject.value:
            result_text.value = "Select Subject"
            page.update()
            return

        if not topic.value:
            result_text.value = "Enter Topic"
            page.update()
            return

        study_state.running = True

        study_state.start_time = datetime.now()

        study_state.current_subject = subject.value

        study_state.current_topic = topic.value

        result_text.value = "Study Session Started"

        page.update()

    def stop_study(e):

        if not study_state.running:
            return

        elapsed = datetime.now() - study_state.start_time

        minutes = max(
            1,
            round(elapsed.total_seconds() / 60)
        )

        add_study_session(
            study_state.current_subject,
            study_state.current_topic,
            minutes,
            str(date.today())
        )

        result_text.value = (
            f"Saved: "
            f"{study_state.current_subject}"
            f" | "
            f"{study_state.current_topic}"
            f" | "
            f"{minutes} mins"
        )

        study_state.running = False

        study_state.start_time = None

        study_state.current_subject = ""

        study_state.current_topic = ""

        timer_text.value = "00:00:00"

        page.update()

    return ft.Column(
        controls=[
            ft.Text(
                "Study Timer",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            subject,

            topic,

            timer_text,

            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Start Study",
                        on_click=start_study
                    ),

                    ft.ElevatedButton(
                        "Stop Study",
                        on_click=stop_study
                    )
                ]
            ),

            result_text
        ]
    )