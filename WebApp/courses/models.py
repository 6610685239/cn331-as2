from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    course_id = models.CharField(max_length=100)  # รหัส
    name = models.CharField(max_length=100)  # ชื่อวิชา
    semester = models.PositiveIntegerField(default=0)  # ภาคการศึกษา
    year = models.PositiveIntegerField(default=0)  # ปีการศึกษา
    capacity = models.PositiveIntegerField(default=0)  # จำนวนที่รับ
    is_open = models.BooleanField(default=True)  # เปิดหรือปิดรายวิชา

    enrolled_users = models.ManyToManyField(
        User, blank=True, related_name="courses"
    )  # ผู้ใช้ที่ขอโควต้า

    def __str__(self):
        return self.name

    def available_slots(self):
        """ตรวจสอบจำนวนที่ยังเหลืออยู่"""
        return self.capacity - self.enrolled_users.count()

    def can_enroll(self):
        """เช็คว่ายังสามารถขอโควต้าได้หรือไม่"""
        return self.is_open and self.available_slots() > 0
