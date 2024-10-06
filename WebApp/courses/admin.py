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
        before_save_users = set(form.instance.enrolled_users.all())
        super().save_related(request, form, formsets, change)
        course = form.instance
        after_save_users = set(course.enrolled_users.all())
        # บันทึกข้อมูลในตาราง Enrollment เมื่อมีการเพิ่มผู้ใช้ในรายวิชาผ่าน admin
        for user in course.enrolled_users.all():
            # ตรวจสอบว่ามีการลงทะเบียนอยู่แล้วหรือไม่
            if not Enrollment.objects.filter(user=user, course=course).exists():
                Enrollment.objects.create(user=user, course=course)

        for user in before_save_users - after_save_users:
            Enrollment.objects.filter(user=user, course=course).delete()


admin.site.register(Course, CourseAdmin)
