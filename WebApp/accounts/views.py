from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, LoginForm
from courses.models import Course
from enrollment.models import Enrollment

# Create your views here.


def login_views(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)  # Ensure you are using your LoginForm
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Check if user is superuser
                if user.is_superuser:
                    return redirect("/admin/")
                else:
                    return redirect("user_home")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("user_home")
        else:
            # Add this to handle invalid form and display errors
            return render(request, "signup.html", {"form": form})
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required  # Ensure that only logged-in users can access this view
def user_home(request):
    open_courses = Course.objects.filter(is_open=True)
    return render(request, "user_home.html", {"courses": open_courses})
