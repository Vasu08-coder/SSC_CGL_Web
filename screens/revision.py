import flet as ft

from database.db import (
    add_revision,
    get_revisions,
    update_revision
)

def revision_view(page):

    topic_field = ft.TextField(
        label="Topic Name"
    )

    revision_list = ft.Column()

    def refresh():

        revision_list.controls.clear()

        revisions = get_revisions()

        for rev in revisions:

            rid, topic, r1, r2, r3 = rev

            revision_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Text(
                                topic,
                                size=18,
                                weight=ft.FontWeight.BOLD
                            ),

                            ft.Row([
                                ft.Checkbox(
                                    label="R1",
                                    value=bool(r1),
                                    on_change=lambda e, x=rid:
                                    update_r(x, 1)
                                ),

                                ft.Checkbox(
                                    label="R2",
                                    value=bool(r2),
                                    on_change=lambda e, x=rid:
                                    update_r(x, 2)
                                ),

                                ft.Checkbox(
                                    label="R3",
                                    value=bool(r3),
                                    on_change=lambda e, x=rid:
                                    update_r(x, 3)
                                )
                            ])
                        ])
                    )
                )
            )

        page.update()

    def update_r(rid, no):
        update_revision(rid, no)
        refresh()

    def add_topic(e):

        if not topic_field.value:
            return

        add_revision(
            topic_field.value
        )

        topic_field.value = ""

        refresh()

    refresh()

    return ft.Column([
        ft.Text(
            "Revision Tracker",
            size=25
        ),

        topic_field,

        ft.ElevatedButton(
            "Add Topic",
            on_click=add_topic
        ),

        ft.Divider(),

        revision_list
    ])