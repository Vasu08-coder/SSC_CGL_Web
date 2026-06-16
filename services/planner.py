from database.db import (
    get_pending_revisions,
    get_completed_tasks,
    get_total_tasks
)

from services.performance import get_difficulty_level

def generate_daily_plan():

    difficulty = get_difficulty_level()
    pending_revisions = get_pending_revisions()
    completed_tasks = get_completed_tasks()
    total_tasks = get_total_tasks()

    plan = []

    # 🔥 PRIORITY 1: Revision pressure system
    if pending_revisions > 0:
        if pending_revisions > 10:
            plan.append(f"URGENT: Revise {pending_revisions} topics (Backlog high)")
        else:
            plan.append(f"Revise {pending_revisions} topics")

    # 🔥 PRIORITY 2: Adaptive workload
    if difficulty == "EASY":
        plan.append("Learn 2 new topics + light practice")
        plan.append("Focus: Concept building")

    elif difficulty == "MEDIUM":
        plan.append("Balanced study: 1 new topic + PYQs")
        plan.append("Mock test practice (partial)")

    else:  # HARD
        plan.append("Full mock test + deep analysis")
        plan.append("Revise weak topics only")

    # 🔥 PRIORITY 3: Daily task check
    if completed_tasks < total_tasks:
        plan.append("Complete pending daily tasks")

    if not plan:
        plan.append("Take full mock test today")

    return {
        "difficulty": difficulty,
        "plan": plan
    }