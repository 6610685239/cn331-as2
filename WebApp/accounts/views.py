from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, LoginForm
from courses.models import Course
from enrollment.models import Enrollment

# Create your views here.


def index(request):
    return render(request, "index.html")


def login_views(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect("/admin/")
                else:
                    return redirect("user_home")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


def user_home(request):
    open_courses = Course.objects.filter(is_open=True)
    return render(request, "user_home.html", {"courses": open_courses})
