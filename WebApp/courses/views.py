from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from django.contrib.auth.decorators import login_required


@login_required
def course_list(request):
    courses = Course.objects.filter(is_open=True)  # แสดงเฉพาะวิชาที่เปิด
    return render(request, "courses/course_list.html", {"courses": courses})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.can_enroll() and request.user not in course.enrolled_users.all():
        course.enrolled_users.add(request.user)  # เพิ่มผู้ใช้ลงในรายวิชาที่ขอโควต้า
        course.save()
        return redirect("course_list")  # กลับไปที่หน้ารายวิชา
    return redirect("course_list")  # ถ้าเต็มหรือขอโควต้าแล้ว
