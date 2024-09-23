# from django.db import models
# from django.contrib.auth.models import User


# # Create your models here.
# class Course(models.Model):
#     number = models.CharField(max_length=100)  # รหัส
#     name = models.CharField(max_length=100)  # ชื่อวิชา
#     semester = models.PositiveIntegerField()  # ภาคการศึกษา
#     year = models.PositiveIntegerField()  # ปีการศึกษา
#     capacity = models.PositiveIntegerField()  # จำนวนที่รับ
#     is_open = models.BooleanField(default=True)  # เปิดหรือปิดรายวิชา

#     def __str__(self):
#         return self.name
