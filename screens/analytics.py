import flet as ft

from database.db import get_topics


def analytics_view():

    topics = get_topics()

    quant_total = 0
    quant_done = 0

    eng_total = 0
    eng_done = 0

    rea_total = 0
    rea_done = 0

    ga_total = 0
    ga_done = 0

    for topic in topics:

        _, name, status = topic

        if name.startswith("Quant"):

            quant_total += 1

            if status == 100:
                quant_done += 1

        elif name.startswith("English"):

            eng_total += 1

            if status == 100:
                eng_done += 1

        elif name.startswith("Reasoning"):

            rea_total += 1

            if status == 100:
                rea_done += 1

        elif name.startswith("GA"):

            ga_total += 1

            if status == 100:
                ga_done += 1

    def calc(done, total):

        if total == 0:
            return 0

        return round((done / total) * 100)

    quant_percent = calc(
        quant_done,
        quant_total
    )

    eng_percent = calc(
        eng_done,
        eng_total
    )

    rea_percent = calc(
        rea_done,
        rea_total
    )

    ga_percent = calc(
        ga_done,
        ga_total
    )

    return ft.Column(
        controls=[

            ft.Text(
                "Analytics",
                size=30,
                weight=ft.FontWeight.BOLD
            ),

            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Text(
                        f"Quant Progress: {quant_percent}%"
                    )
                )
            ),

            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Text(
                        f"English Progress: {eng_percent}%"
                    )
                )
            ),

            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Text(
                        f"Reasoning Progress: {rea_percent}%"
                    )
                )
            ),

            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Text(
                        f"GA Progress: {ga_percent}%"
                    )
                )
            )
        ]
    )