from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "predicted_strength",
        "age",
        "created_at",
    )

    search_fields = ("user__username",)

    list_filter = ("created_at",)