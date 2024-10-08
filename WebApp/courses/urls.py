from django.urls import path
from . import views

urlpatterns = [
    path("", views.course_list, name="course_list"),  # ดูรายการวิชา
    path(
        "enroll/<int:course_id>/", views.enroll_course, name="enroll_course"
    ),  # ขอโควต้า
]
