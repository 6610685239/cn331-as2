from django.contrib import admin
from django.contrib.auth.models import User
from .models import Course
from enrollment.models import Enrollment


class EnrollmentInline(admin.TabularInline):
    model = Course.enrolled_users.through
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_id",
        "name",
        "semester",
        "year",
        "capacity",
        "is_open",
        "get_enrolled_users",
    )  # แสดงฟิลด์ที่ต้องการในหน้า Admin
    inlines = [EnrollmentInline]
    list_filter = ("is_open",)  # กรองตามสถานะเปิด/ปิดรายวิชา
    search_fields = ("name",)  # ค้นหาด้วยชื่อวิชา

    def get_enrolled_users(self, obj):
        return " , ".join([user.username for user in obj.enrolled_users.all()])

    get_enrolled_users.short_description = "Enrolled Users"

    def save_related(self, request, form, formsets, change):
        # Retrieve the set of users before saving changes
        course = form.instance
        before_save_users = set(course.enrolled_users.all())

        # Save the form and formsets (i.e., apply changes to `enrolled_users`)
        super().save_related(request, form, formsets, change)

        # Retrieve the updated set of users after saving changes
        after_save_users = set(course.enrolled_users.all())

        # Handle added users (create Enrollment records)
        for user in after_save_users - before_save_users:
            if not Enrollment.objects.filter(user=user, course=course).exists():
                Enrollment.objects.create(user=user, course=course)

        # Handle removed users (delete Enrollment records)
        for user in before_save_users - after_save_users:
            Enrollment.objects.filter(user=user, course=course).delete()

    get_enrolled_users.short_description = "Enrolled Users"


admin.site.register(Course, CourseAdmin)
