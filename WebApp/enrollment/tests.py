from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course
from enrollment.models import Enrollment
from django.contrib.messages import get_messages


class EnrollmentModelTest(TestCase):
    def setUp(self):
        # Set up a user and course for testing Enrollment
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.course = Course.objects.create(
            course_id="C101",
            name="Mathematics",
            semester=1,
            year=2024,
            capacity=30,
            is_open=True,
        )

    def test_enrollment_str_method(self):
        # Test the __str__ method of Enrollment model
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        self.assertEqual(str(enrollment), f"{self.user.username} - {self.course.name}")


class EnrollmentViewTest(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        # Create an open course
        self.course = Course.objects.create(
            course_id="C101",
            name="Open Course",
            semester=1,
            year=2024,
            capacity=30,
            is_open=True,
        )

    def test_request_quota_success(self):
        # Test a successful quota request
        response = self.client.post(reverse("request_quota", args=[self.course.id]))
        self.assertRedirects(response, reverse("user_home"))

        # Check if Enrollment record is created
        enrollment = Enrollment.objects.filter(user=self.user, course=self.course)
        self.assertTrue(enrollment.exists())
        self.assertIn(self.user, self.course.enrolled_users.all())

        # Confirm success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Request quota success!")

    def test_request_quota_already_requested(self):
        # Create an initial enrollment to simulate an existing request
        Enrollment.objects.create(user=self.user, course=self.course)

        response = self.client.post(reverse("request_quota", args=[self.course.id]))
        self.assertRedirects(response, reverse("user_home"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "You already requested the quota!")

    def test_request_quota_course_closed(self):
        # Close the course and try requesting quota
        self.course.is_open = False
        self.course.save()

        response = self.client.post(reverse("request_quota", args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "วิชานี้ไม่เปิดให้ขอโควต้าในขณะนี้!")

    def test_request_quota_course_full(self):
        # Fill the course to capacity and attempt to request quota
        for i in range(self.course.capacity):
            user = User.objects.create_user(username=f"user{i}", password="password123")
            self.course.enrolled_users.add(user)

        response = self.client.post(reverse("request_quota", args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "วิชานี้ไม่เปิดให้ขอโควต้าในขณะนี้!")
