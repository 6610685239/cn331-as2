from django.urls import path
from .views import request_quota

urlpatterns = [
    path("request-quota/<int:course_id>/", request_quota, name="request_quota"),
]
