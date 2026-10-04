from django.db.models import Avg, Max
from prediction.models import Prediction
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, UserUpdateForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard_view(request):
    if request.user.is_staff:
        return redirect("admin_dashboard:dashboard")

    predictions = Prediction.objects.filter(
        user=request.user
    ).order_by("-created_at")

    total_predictions = predictions.count()

    stats = predictions.aggregate(
        average_strength=Avg("predicted_strength"),
        highest_strength=Max("predicted_strength"),
    )

    latest_prediction = predictions.first()
    recent_predictions = predictions[:5]

    context = {
        "total_predictions": total_predictions,
        "average_strength": stats["average_strength"],
        "highest_strength": stats["highest_strength"],
        "latest_prediction": latest_prediction,
        "recent_predictions": recent_predictions,
    }

    return render(
        request,
        "accounts/dashboard.html",
        context
    )

@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect("accounts:profile")

    else:
        form = UserUpdateForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/profile.html",
        {"form": form}
    )
