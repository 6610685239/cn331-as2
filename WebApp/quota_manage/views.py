from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from enrollment.models import Enrollment
from courses.models import Course
from django.contrib import messages

# Create your views here.


@login_required
def quota_list(request):
    user = request.user
    enrollments = Enrollment.objects.filter(user=request.user)

    return render(request, "quota_manage/quota_list.html", {"enrollments": enrollments})


@login_required
def cancel_quota(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)
    course = enrollment.course

    enrollment.delete()
    course.enrolled_users.remove(request.user)
    course.save()

    messages.success(request, "ยกเลิกการลงทะเบียนสำเร็จ")
    return redirect("quota_list")  # Ensure this points to your quota_list view
