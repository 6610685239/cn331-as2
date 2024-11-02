# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from courses.models import Course
# from enrollment.models import Enrollment
# from django.contrib.messages import get_messages


# class CourseModelTest(TestCase):
#     def setUp(self):
#         # Create a user and a course for testing purposes
#         self.user = User.objects.create_user(username="testuser", password="zazazaza")
#         self.course = Course.objects.create(
#             course_id="C101",
#             name="Mathematics",
#             semester=1,
#             year=2024,
#             capacity=30,
#             is_open=True,
#         )

#     def test_course_str_method(self):
#         self.assertEqual(str(self.course), "Mathematics")

#     def test_available_slots_property(self):
#         self.assertEqual(self.course.available_slots, 30)
#         self.course.enrolled_users.add(self.user)
#         self.assertEqual(self.course.available_slots, 29)

#     def test_enroll_user_method(self):
#         # Test successful enrollment
#         enrolled = self.course.enroll_user(self.user)
#         self.assertTrue(enrolled)
#         self.assertIn(self.user, self.course.enrolled_users.all())

#         # Test re-enrollment should return False
#         enrolled_again = self.course.enroll_user(self.user)
#         self.assertFalse(enrolled_again)

#         # Test enrollment failure when course is full
#         for i in range(self.course.capacity):
#             user = User.objects.create_user(username=f"user{i}", password="zazazaza")
#             self.course.enrolled_users.add(user)

#         # Trying to enroll another user when full should return False
#         new_user = User.objects.create_user(username="new_user", password="zazazaza")
#         full_enrollment_attempt = self.course.enroll_user(new_user)
#         self.assertFalse(full_enrollment_attempt)


# class EnrollmentViewTest(TestCase):
#     def setUp(self):
#         # Create a user and log them in for testing views
#         self.user = User.objects.create_user(username="testuser", password="zazazaza")
#         self.client.login(username="testuser", password="zazazaza")

#         # Create an open course for enrollment tests
#         self.course = Course.objects.create(
#             course_id="C101",
#             name="Open Course",
#             semester=1,
#             year=2024,
#             capacity=30,
#             is_open=True,
#         )

#     def test_request_quota_success(self):
#         # Test successfully requesting quota for an open course with available slots
#         response = self.client.post(reverse("request_quota", args=[self.course.id]))
#         self.assertRedirects(response, reverse("user_home"))

#         # Check if the user is enrolled and an Enrollment object is created
#         enrollment = Enrollment.objects.filter(user=self.user, course=self.course)
#         self.assertTrue(enrollment.exists())
#         self.assertIn(self.user, self.course.enrolled_users.all())

#         # Confirm success message in response
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "Request quota success!")

#     def test_request_quota_already_requested(self):
#         # Create an existing enrollment to simulate already requested quota
#         Enrollment.objects.create(user=self.user, course=self.course)

#         response = self.client.post(reverse("request_quota", args=[self.course.id]))
#         self.assertRedirects(response, reverse("user_home"))
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "You already requested the quota!")

#     def test_request_quota_course_closed(self):
#         # Close the course and attempt to request quota
#         self.course.is_open = False
#         self.course.save()

#         response = self.client.post(reverse("request_quota", args=[self.course.id]))
#         self.assertEqual(response.status_code, 200)
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "วิชานี้ไม่เปิดให้ขอโควต้าในขณะนี้!")

#     def test_request_quota_course_full(self):
#         # Fill the course to capacity
#         for i in range(self.course.capacity):
#             user = User.objects.create_user(username=f"user{i}", password="zazazaza")
#             self.course.enrolled_users.add(user)

#         response = self.client.post(reverse("request_quota", args=[self.course.id]))
#         self.assertEqual(response.status_code, 200)
#         messages = list(get_messages(response.wsgi_request))
#         self.assertEqual(str(messages[0]), "วิชานี้ไม่เปิดให้ขอโควต้าในขณะนี้!")
