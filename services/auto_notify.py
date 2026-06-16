from services.notification import show_notification
from services.planner import generate_daily_plan

def send_adaptive_plan():
    data = generate_daily_plan()

    plan_text = "\n".join(
        f"{i+1}. {task}" for i, task in enumerate(data["plan"])
    )

    show_notification(
        f"📊 SSC Plan ({data['difficulty']})",
        plan_text
    )