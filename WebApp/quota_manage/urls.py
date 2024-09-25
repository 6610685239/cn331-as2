from django.urls import path
from .views import quota_list, cancel_quota

urlpatterns = [
    path('', quota_list, name='quota_list'),
    path('cancel/<int:enrollment_id>/', cancel_quota, name='cancel_quota'),
]