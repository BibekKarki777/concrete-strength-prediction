from django.urls import path

from . import views


app_name = "prediction"

urlpatterns = [
    path(
        "<int:pk>/delete/",
        views.delete_view,
        name="delete",
    ),
    path("new/", views.predict_view, name="predict"),
    path("history/", views.history_view, name="history"),
    path("analytics/", views.analytics_view, name="analytics"),

    path(
        "<int:pk>/result/",
        views.result_view,
        name="result"
    ),
]