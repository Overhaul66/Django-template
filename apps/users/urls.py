from django.urls import path

from .views import user_profile

urlpatterns = [
    path("users/me/", user_profile, name="user-profile"),
]
