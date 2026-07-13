from celery import shared_task
from apps.notifications.services import send_notification
from apps.users.models import CustomUser

@shared_task
def send_reminder_notification_task(user_id, title, message):
    """
    Background celery task to send a notification to a specific user.
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        send_notification(user, title, message)
        return True
    except CustomUser.DoesNotExist:
        return False
