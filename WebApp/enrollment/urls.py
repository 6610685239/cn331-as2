from django.urls import path
from .views import request_quota
from accounts.views import user_home

urlpatterns = [
    path("request-quota/<int:course_id>/", request_quota, name="request_quota"),
    path('user-home/', user_home, name='user_home'),
]
