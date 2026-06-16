import flet as ft
from datetime import date

from database.db import (
    add_planned_task,
    get_planned_tasks
)


def planner_view(page):

    task_list = ft.Column()

    subject_dropdown = ft.Dropdown(
        width=250,
        options=[
            ft.dropdown.Option("Quant"),
            ft.dropdown.Option("Reasoning"),
            ft.dropdown.Option("English"),
            ft.dropdown.Option("GA"),
        ]
    )

    topic_field = ft.TextField(
        label="Topic",
        width=300
    )

    def refresh_tasks():

        task_list.controls.clear()

        tasks = get_planned_tasks()

        for task in tasks:

            _, subject, topic = task

            task_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Text(
                            f"{subject} - {topic}"
                        )
                    )
                )
            )

        page.update()

    def save_plan(e):

        if not subject_dropdown.value:
            return

        if not topic_field.value:
            return

        add_planned_task(
            subject_dropdown.value,
            topic_field.value,
            str(date.today())
        )

        topic_field.value = ""

        refresh_tasks()

    refresh_tasks()

    return ft.Column(
        controls=[
            ft.Text(
                "Plan Tomorrow",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            subject_dropdown,

            topic_field,

            ft.ElevatedButton(
                "Add To Plan",
                on_click=save_plan
            ),

            ft.Divider(),

            ft.Text(
                "Planned Tasks",
                size=20,
                weight=ft.FontWeight.BOLD
            ),

            task_list
        ]
    )