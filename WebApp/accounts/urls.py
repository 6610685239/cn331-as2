from django.urls import path
from . import views
from .views import user_home

urlpatterns = [
    path("", views.login_views, name="home"),
    path("login/", views.login_views, name="login"),
    path("user-home/", views.user_home, name="user_home"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
]
