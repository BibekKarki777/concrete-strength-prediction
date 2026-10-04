import json

from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Max, Q
from django.shortcuts import get_object_or_404, redirect, render

from prediction.models import Prediction


@staff_member_required
def dashboard_view(request):
    predictions = Prediction.objects.all().order_by("-created_at")

    stats = predictions.aggregate(
        average_strength=Avg("predicted_strength"),
        highest_strength=Max("predicted_strength"),
    )

    context = {
        "total_users": User.objects.count(),
        "total_predictions": predictions.count(),
        "average_strength": stats["average_strength"],
        "highest_strength": stats["highest_strength"],
        "recent_predictions": predictions[:5],
    }

    return render(
        request,
        "admin_dashboard/dashboard.html",
        context
    )

@staff_member_required
def users_view(request):
    search_query = request.GET.get("search", "")

    users = User.objects.annotate(
        prediction_count=Count("predictions")
    ).order_by("-date_joined")

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
        )

    context = {
        "users": users,
        "search_query": search_query,
    }

    return render(
        request,
        "admin_dashboard/users.html",
        context
    )

@staff_member_required
def predictions_view(request):
    search_query = request.GET.get("search", "").strip()
    user_filter = request.GET.get("user", "")

    predictions = Prediction.objects.select_related(
        "user"
    ).order_by("-created_at")

    if search_query:
        predictions = predictions.filter(
            Q(user__username__icontains=search_query)
            | Q(user__email__icontains=search_query)
        )

    if user_filter:
        predictions = predictions.filter(
            user_id=user_filter
        )

    users = User.objects.order_by("username")

    context = {
        "predictions": predictions,
        "users": users,
        "search_query": search_query,
        "user_filter": user_filter,
    }

    return render(
        request,
        "admin_dashboard/predictions.html",
        context
    )


@staff_member_required
def prediction_detail_view(request, pk):
    prediction = get_object_or_404(
        Prediction.objects.select_related("user"),
        pk=pk
    )

    return render(
        request,
        "admin_dashboard/prediction_detail.html",
        {"prediction": prediction}
    )

@staff_member_required
def model_info_view(request):
    model_info_path = (
        settings.BASE_DIR
        / "ml"
        / "models"
        / "model_info.json"
    )

    model_info = None
    error_message = None

    try:
        with open(model_info_path, "r", encoding="utf-8") as file:
            model_info = json.load(file)

    except FileNotFoundError:
        error_message = "Model information file was not found."

    except json.JSONDecodeError:
        error_message = "Model information file contains invalid JSON."

    context = {
        "model_info": model_info,
        "error_message": error_message,
    }

    return render(
        request,
        "admin_dashboard/model_info.html",
        context
    )

@staff_member_required
@require_POST
def delete_prediction_view(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk)
    prediction.delete()
    messages.success(request, "Prediction deleted successfully.")
    if request.POST.get("return_to") == "dashboard":
        return redirect("admin_dashboard:dashboard")
    return redirect("admin_dashboard:predictions")
