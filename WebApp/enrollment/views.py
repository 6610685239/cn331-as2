from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Enrollment
from django.contrib import messages

@login_required
def request_quota(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # ตรวจสอบว่ายังมีที่ว่างและเปิดอยู่
    if course.can_enroll():
        # ตรวจสอบว่าผู้ใช้ยังไม่ได้ขอในวิชานี้
        if not Enrollment.objects.filter(user=user, course=course).exists():
            Enrollment.objects.create(user=user, course=course)
            course.enrolled_users.add(user)
            course.save()
            messages.success(request, 'ขอโควต้าสำเร็จ!')
            return redirect("user_home")  # ส่งผู้ใช้กลับไปยังหน้า user_home
        else:
            messages.warning(request, 'คุณได้ขอโควต้าในวิชานี้แล้ว!')
    else:
        messages.error(request, 'วิชานี้ไม่เปิดให้ขอโควต้าในขณะนี้!')
    return render(request, "enrollment/course_list.html", {"course": course})

