from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm
from courses.models import Course


class ViewsTest(TestCase):
    def setUp(self):
        # Set up user and course data for testing
        self.user = User.objects.create_user(username="testuser", password="zazazaza")
        self.superuser = User.objects.create_superuser(
            username="adminuser", password="admincn331"
        )

        self.course = Course.objects.create(
            course_id="C101",
            name="Mathematics",
            semester=1,
            year=2024,
            capacity=30,
            is_open=True,
        )

    # Test login view (lines 16-34)
    def test_login_view_get(self):
        # Test GET request for login view
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_view_post_success(self):
        # Test POST request with valid credentials
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "zazazaza"}
        )
        self.assertRedirects(response, reverse("user_home"))

    def test_login_view_post_fail(self):
        # Test POST request with invalid credentials
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "zazazaza55"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
        self.assertContains(response, "Please enter a correct username and password.")

    def test_login_superuser_redirect(self):
        # Test that a superuser is redirected to the admin page upon login
        response = self.client.post(
            reverse("login"), {"username": "adminuser", "password": "admincn331"}
        )
        self.assertRedirects(response, "/admin/")

    # Test signup view (lines 38-50)
    def test_signup_view_get(self):
        # Test GET request for signup view
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    def test_signup_view_post_success(self):
        # Test POST request with valid signup data
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "password1": "zazazaza",
                "password2": "zazazaza",
            },
        )
        self.assertRedirects(response, reverse("user_home"))

    def test_signup_view_post_fail(self):
        # Test POST request with invalid signup data (password mismatch)
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "password1": "zazazaza",
                "password2": "password321",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    # Test logout view (lines 56-57)
    def test_logout_view(self):
        # Login first, then logout to test the view
        self.client.login(username="testuser", password="zazazaza")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    # Test user home view (lines 61-62)
    def test_user_home_view_logged_in(self):
        # Only accessible to logged-in users, so login first
        self.client.login(username="testuser", password="zazazaza")
        response = self.client.get(reverse("user_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_home.html")
        self.assertContains(response, "Mathematics")
