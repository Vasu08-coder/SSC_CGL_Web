from database.db import (
    get_completed_topics_count,
    get_total_topics_count,
    get_latest_mock_score
)

def get_performance_level():
    completed = get_completed_topics_count()
    total = get_total_topics_count()

    progress = (completed / total) * 100 if total > 0 else 0
    mock_score = get_latest_mock_score()

    # Normalize score (assume /200 exam)
    score_percent = (mock_score / 200) * 100 if mock_score else 0

    return {
        "progress": progress,
        "mock_score": score_percent
    }


def get_difficulty_level():
    perf = get_performance_level()

    if perf["mock_score"] < 40 or perf["progress"] < 30:
        return "EASY"
    elif perf["mock_score"] < 70 or perf["progress"] < 70:
        return "MEDIUM"
    else:
        return "HARD"