from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import CustomAuthenticationForm


app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=CustomAuthenticationForm,
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path(
        "dashboard/",
        views.dashboard_view,
        name="dashboard",
    ),

    path(
        "profile/",
        views.profile_view,
        name="profile",
    ),
]
