from .models import Notification

def send_notification(user, title, message):
    """
    Creates and saves a notification to the database for the user.
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
    # In a production environment, we could dispatch Celery tasks to send emails or SMS here
    return notification
