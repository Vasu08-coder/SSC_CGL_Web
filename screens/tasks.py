import flet as ft
from datetime import date

from database.db import (
    add_task,
    get_tasks,
    complete_task
)


def tasks_view(page):

    task_list = ft.Column()

    subject_dropdown = ft.Dropdown(
        width=200,
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

    def load_tasks():
        task_list.controls.clear()

        tasks = get_tasks()

        for task in tasks:
            task_id, subject, topic, completed = task

            checkbox = ft.Checkbox(
                label=f"{subject} - {topic}",
                value=bool(completed),

                on_change=lambda e, tid=task_id:
                mark_complete(tid)
            )

            task_list.controls.append(checkbox)

        page.update()

    def mark_complete(task_id):
        complete_task(task_id)
        load_tasks()

    def save_task(e):

        if not subject_dropdown.value:
            return

        if not topic_field.value:
            return

        add_task(
            subject_dropdown.value,
            topic_field.value,
            str(date.today())
        )

        topic_field.value = ""

        load_tasks()

    add_button = ft.ElevatedButton(
        "Add Task",
        on_click=save_task
    )

    load_tasks()

    return ft.Column(
        controls=[
            ft.Text(
                "Daily Tasks",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            subject_dropdown,
            topic_field,
            add_button,

            ft.Divider(),

            task_list
        ]
    )