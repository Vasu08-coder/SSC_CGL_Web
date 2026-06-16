import flet as ft
from datetime import date

from database.db import (
    add_mock_test,
    get_mock_tests
)

def mocks_view(page):

    test_name = ft.TextField(
        label="Mock Name"
    )

    score = ft.TextField(
        label="Score"
    )

    mock_list = ft.Column()

    def refresh():

        mock_list.controls.clear()

        tests = get_mock_tests()

        for t in tests:

            name, marks, dt = t

            mock_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            ft.Text(name),
                            ft.Text(f"Score: {marks}"),
                            ft.Text(dt)
                        ])
                    )
                )
            )

        page.update()

    def save_mock(e):

        add_mock_test(
            test_name.value,
            int(score.value),
            str(date.today())
        )

        test_name.value = ""
        score.value = ""

        refresh()

    refresh()

    return ft.Column([
        ft.Text(
            "Mock Tests",
            size=25
        ),

        test_name,
        score,

        ft.ElevatedButton(
            "Save Mock",
            on_click=save_mock
        ),

        ft.Divider(),

        mock_list
    ])