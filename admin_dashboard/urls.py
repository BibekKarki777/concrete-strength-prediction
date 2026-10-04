from django.urls import path

from . import views


app_name = "admin_dashboard"

urlpatterns = [
    path(
        "predictions/<int:pk>/delete/",
        views.delete_prediction_view,
        name="delete_prediction",
    ),
    path("", views.dashboard_view, name="dashboard"),

    path(
        "users/",
        views.users_view,
        name="users"
    ),

    path(
        "predictions/",
        views.predictions_view,
        name="predictions"
    ),

    path(
        "predictions/<int:pk>/",
        views.prediction_detail_view,
        name="prediction_detail"
    ),
    
    path(
        "model-info/",
        views.model_info_view,
        name="model_info"
    ),
]