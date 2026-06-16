import flet as ft
from database.db import get_all_sessions


def history_view():

    sessions = get_all_sessions()

    session_list = []

    for session in sessions:
        subject, topic, minutes, study_date = session

        card = ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column(
                    [
                        ft.Text(
                            f"{subject}",
                            weight=ft.FontWeight.BOLD,
                            size=18,
                        ),
                        ft.Text(f"Topic: {topic}"),
                        ft.Text(f"Study Time: {minutes} mins"),
                        ft.Text(f"Date: {study_date}"),
                    ]
                ),
            )
        )

        session_list.append(card)

    return ft.Column(
        controls=[
            ft.Text(
                "Study History",
                size=28,
                weight=ft.FontWeight.BOLD,
            ),
            *session_list,
        ]
    )