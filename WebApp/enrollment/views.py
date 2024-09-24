from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Enrollment


@login_required
def request_quota(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # ตรวจสอบว่ายังมีที่ว่างและเปิดอยู่
    if course.can_enroll():
        # ตรวจสอบว่าผู้ใช้ยังไม่ได้ขอในวิชานี้
        if not Enrollment.objects.filter(user=user, course=course).exists():
            Enrollment.objects.create(user=user, course=course)
            return redirect("user_home")  # ส่งผู้ใช้กลับไปยังหน้า user_home
    return render(request, "enrollment/course_full.html", {"course": course})
