import flet as ft

from database.db import create_tables
from screens.dashboard import dashboard_view
from screens.tasks import tasks_view
from screens.timer import timer_view
from screens.history import history_view
from screens.planner import planner_view
from screens.syllabus import syllabus_view
from screens.mocks import mocks_view
from screens.revision import revision_view
from screens.analytics import analytics_view
from services.notification import show_notification


def load_dashboard():
    pending_revisions = 8
    todays_targets = 3

    show_notification(
        "SSC CGL Tracker",
        f"Pending: {pending_revisions} | Targets Left: {todays_targets}"
    )


def main(page: ft.Page):

    create_tables()

    page.title = "SSC CGL Tracker"

    page.theme_mode = ft.ThemeMode.LIGHT

    page.theme = ft.Theme(
        color_scheme_seed="#4F46E5"
    )

    page.bgcolor = "#F3F4F6"

    page.padding = 15
    page.scroll = "auto"

    content = ft.Column(
        expand=True,
        spacing=15
    )

    def show_dashboard(e=None):
        content.controls.clear()
        content.controls.append(dashboard_view())
        page.update()

    def show_tasks(e=None):
        content.controls.clear()
        content.controls.append(tasks_view(page))
        page.update()

    def show_timer(e=None):
        content.controls.clear()
        content.controls.append(timer_view(page))
        page.update()

    def show_history(e=None):
        content.controls.clear()
        content.controls.append(history_view())
        page.update()

    def show_planner(e=None):
        content.controls.clear()
        content.controls.append(planner_view(page))
        page.update()

    def show_syllabus(e=None):
        content.controls.clear()
        content.controls.append(syllabus_view(page))
        page.update()

    def show_revision(e=None):
        content.controls.clear()
        content.controls.append(revision_view(page))
        page.update()

    def show_mocks(e=None):
        content.controls.clear()
        content.controls.append(mocks_view(page))
        page.update()

    def show_analytics(e=None):
        content.controls.clear()
        content.controls.append(analytics_view())
        page.update()

    nav = ft.Row(
        scroll="auto",
        controls=[

            ft.ElevatedButton(
                "Dashboard",
                icon=ft.Icons.HOME,
                bgcolor="#4F46E5",
                color="white",
                on_click=show_dashboard
            ),

            ft.ElevatedButton(
                "Tasks",
                icon=ft.Icons.CHECKLIST,
                bgcolor="#10B981",
                color="white",
                on_click=show_tasks
            ),

            ft.ElevatedButton(
                "Timer",
                icon=ft.Icons.TIMER,
                bgcolor="#F59E0B",
                color="white",
                on_click=show_timer
            ),

            ft.ElevatedButton(
                "History",
                icon=ft.Icons.HISTORY,
                bgcolor="#EF4444",
                color="white",
                on_click=show_history
            ),

            ft.ElevatedButton(
                "Planner",
                icon=ft.Icons.CALENDAR_MONTH,
                bgcolor="#06B6D4",
                color="white",
                on_click=show_planner
            ),

            ft.ElevatedButton(
                "Syllabus",
                icon=ft.Icons.MENU_BOOK,
                bgcolor="#8B5CF6",
                color="white",
                on_click=show_syllabus
            ),

            ft.ElevatedButton(
                "Revision",
                icon=ft.Icons.REPLAY,
                bgcolor="#EC4899",
                color="white",
                on_click=show_revision
            ),

            ft.ElevatedButton(
                "Mocks",
                icon=ft.Icons.QUIZ,
                bgcolor="#14B8A6",
                color="white",
                on_click=show_mocks
            ),

            ft.ElevatedButton(
                "Analytics",
                icon=ft.Icons.BAR_CHART,
                bgcolor="#F97316",
                color="white",
                on_click=show_analytics
            ),
        ]
    )

    title = ft.Container(
    content=ft.Column(
        controls=[
            ft.Text(
                "SSC CGL Tracker",
                size=28,
                weight=ft.FontWeight.BOLD,
                color="#111827"
            ),
            ft.Text(
                "Track • Study • Revise • Crack SSC CGL",
                size=14,
                color="#6B7280"
            )
        ]
    )
)

    page.add(
        title,
        nav,
        ft.Divider(),
        content
    )

    load_dashboard()
    show_dashboard()


ft.app(target=main)