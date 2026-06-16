from plyer import notification


def show_notification(title, message):

    notification.notify(
        title=title,
        message=message,
        timeout=10
    )
from services.notification import show_notification

show_notification(
    "SSC CGL Tracker",
    "Today's Targets Pending!"
)