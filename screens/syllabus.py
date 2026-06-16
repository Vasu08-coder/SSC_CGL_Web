import flet as ft

from database.db import (
    add_topic,
    get_topics,
    complete_topic
)


def syllabus_view(page):

    topic_list = ft.Column()

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

    progress_text = ft.Text(
        "Completion: 0%",
        size=20,
        weight=ft.FontWeight.BOLD
    )

    def refresh_topics():

        topic_list.controls.clear()

        topics = get_topics()

        total = len(topics)
        completed = 0

        for topic in topics:

            topic_id, topic_name, status = topic

            if status == 100:
                completed += 1

            topic_list.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(topic_name),

                        ft.Checkbox(
                            value=(status == 100),
                            on_change=lambda e, tid=topic_id:
                            mark_complete(tid)
                        )
                    ]
                )
            )

        percent = 0

        if total > 0:
            percent = round(
                (completed / total) * 100
            )

        progress_text.value = (
            f"Completion: {percent}%"
        )

        page.update()

    def add_new_topic(e):

        if not subject_dropdown.value:
            return

        if not topic_field.value:
            return

        add_topic(
            subject_dropdown.value,
            topic_field.value
        )

        topic_field.value = ""

        refresh_topics()

    def mark_complete(topic_id):

        complete_topic(topic_id)

        refresh_topics()

    refresh_topics()

    return ft.Column(
        controls=[
            ft.Text(
                "SSC CGL Syllabus Tracker",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            subject_dropdown,

            topic_field,

            ft.ElevatedButton(
                "Add Topic",
                on_click=add_new_topic
            ),

            ft.Divider(),

            progress_text,

            ft.Divider(),

            topic_list
        ]
    )