from django.contrib import admin
from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_id",
        "name",
        "semester",
        "year",
        "capacity",
        "is_open",
    )  # แสดงฟิลด์ที่ต้องการในหน้า Admin
    list_filter = ("is_open",)  # กรองตามสถานะเปิด/ปิดรายวิชา
    search_fields = ("name",)  # ค้นหาด้วยชื่อวิชา


admin.site.register(Course, CourseAdmin)
