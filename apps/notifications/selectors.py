from .models import Notification

def get_unread_notifications(user):
    return Notification.objects.filter(user=user, is_read=False)

def get_user_notifications(user):
    return Notification.objects.filter(user=user)
