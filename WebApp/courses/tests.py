from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course
from django.contrib.messages import get_messages


class CourseModelTest(TestCase):
    def setUp(self):
        # Create a user and a course for testing purposes
        self.user = User.objects.create_user(username="testuser", password="zazazaza")
        self.course = Course.objects.create(
            course_id="CN331",
            name="Django",
            semester=1,
            year=2024,
            capacity=30,
            is_open=True,
        )

    def test_course_str_method(self):
        self.assertEqual(str(self.course), "Django")

    def test_available_slots_property(self):
        self.assertEqual(self.course.available_slots, 30)
        self.course.enrolled_users.add(self.user)
        self.assertEqual(self.course.available_slots, 29)

    def test_enroll_user_method(self):
        # Test successful enrollment
        enrolled = self.course.enroll_user(self.user)
        self.assertTrue(enrolled)
        self.assertIn(self.user, self.course.enrolled_users.all())

        # Test re-enrollment should return False
        enrolled_again = self.course.enroll_user(self.user)
        self.assertFalse(enrolled_again)

        # Test enrollment failure when course is full
        for i in range(self.course.capacity):
            user = User.objects.create_user(username=f"user{i}", password="zazazaza")
            self.course.enrolled_users.add(user)

        # Trying to enroll another user when full should return False
        new_user = User.objects.create_user(username="new_user", password="zazazaza")
        full_enrollment_attempt = self.course.enroll_user(new_user)
        self.assertFalse(full_enrollment_attempt)
