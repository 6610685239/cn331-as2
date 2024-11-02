from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from enrollment.models import Enrollment
from courses.models import Course


class QuotaManageViewTest(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        # Create a course and an enrollment for the user
        self.course = Course.objects.create(
            course_id="CN331",
            name="Django",
            semester=1,
            year=2024,
            capacity=30,
            is_open=True,
        )
        self.enrollment = Enrollment.objects.create(user=self.user, course=self.course)

    def test_quota_list_view(self):
        # Test accessing the quota list
        response = self.client.get(reverse("quota_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quota_manage/quota_list.html")

        # Check that the enrollment appears in the context
        self.assertIn(self.enrollment, response.context["enrollments"])

    def test_cancel_quota_success(self):
        # Test canceling an enrollment
        response = self.client.post(reverse("cancel_quota", args=[self.enrollment.id]))
        self.assertRedirects(response, reverse("quota_list"))

        # Verify the enrollment was deleted and user removed from enrolled_users
        enrollment_exists = Enrollment.objects.filter(id=self.enrollment.id).exists()
        self.assertFalse(enrollment_exists)
        self.assertNotIn(self.user, self.course.enrolled_users.all())

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "ยกเลิกการลงทะเบียนสำเร็จ")

    def test_cancel_quota_not_found(self):
        # Test canceling an enrollment that does not exist (or belongs to a different user)
        other_user = User.objects.create_user(
            username="otheruser", password="password123"
        )
        other_enrollment = Enrollment.objects.create(
            user=other_user, course=self.course
        )

        # Try to cancel `other_enrollment` with `self.user`, expecting a 404
        response = self.client.post(reverse("cancel_quota", args=[other_enrollment.id]))
        self.assertEqual(response.status_code, 404)
