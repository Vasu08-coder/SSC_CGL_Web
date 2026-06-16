import flet as ft
from datetime import date
from config import EXAM_DATE

from services.notification import show_notification
from database.db import (
    get_completed_topics_count,
    get_total_topics_count,
    get_pending_revisions,
    get_latest_mock_score,
    get_completed_tasks,
    get_total_tasks
)

from services.auto_notify import send_adaptive_plan

import flet as ft
from datetime import date
from config import EXAM_DATE

from database.db import (
    get_completed_topics_count,
    get_total_topics_count,
    get_pending_revisions,
    get_latest_mock_score,
    get_completed_tasks,
    get_total_tasks
)

from services.notification import show_notification


def dashboard_view():

    # ================= DATA =================
    completed_topics = get_completed_topics_count()
    total_topics = get_total_topics_count()

    pending = get_pending_revisions()

    progress = round((completed_topics / total_topics) * 100) if total_topics > 0 else 0
    days_left = (EXAM_DATE - date.today()).days

    # ================= ONE-TIME ALERT =================
    # (IMPORTANT: keep it minimal for mobile stability)
    if pending > 0:
        show_notification(
            "SSC CGL Tracker",
            f"You have {pending} pending revisions"
        )

    # ================= UI =================
    return ft.Column(
        controls=[

            ft.Text(
                "SSC CGL TRACKER",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            ft.Divider(),

            ft.Text(f"Days Left: {days_left}", size=18),
            ft.Text(f"Progress: {progress}%"),
            ft.Text(f"Topics: {completed_topics}/{total_topics}"),

            ft.Text(f"Today's Tasks: {get_completed_tasks()}/{get_total_tasks()}"),
            ft.Text(f"Pending Revisions: {pending}"),
            ft.Text(f"Latest Mock: {get_latest_mock_score()}"),

        ]
    )