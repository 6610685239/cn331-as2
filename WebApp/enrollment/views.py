from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses.models import Course
from .models import Enrollment
from django.contrib import messages
@login_required
def request_quota(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # Check if there are available slots and the course is open
    if course.can_enroll():
        # Check if the user has not already requested for this course
        if not Enrollment.objects.filter(user=user, course=course).exists():
            Enrollment.objects.create(user=user, course=course)
            course.enrolled_users.add(user)
            course.save()
            messages.success(request, 'Request quota success!')
            return redirect("user_home")  # Redirect to user home page
        else:
            messages.warning(request, 'You already requested the quota!')
            return redirect("user_home")  # User has already requested
    else:
        messages.error(request, 'วิชานี้ไม่เปิดให้ขอโควต้าในขณะนี้!')  # Course not open for requests

    return render(request, "enrollment/course_list.html", {"course": course})


