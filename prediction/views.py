from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PredictionForm
from .models import Prediction
from .services.predictor import predict_strength
from django.db.models import Avg, Max, Min


@login_required
def predict_view(request):
    if request.method == "POST":
        form = PredictionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            predicted_strength = predict_strength(data)

            prediction = Prediction.objects.create(
                user=request.user,
                cement=data["cement"],
                blast_furnace_slag=data["blast_furnace_slag"],
                fly_ash=data["fly_ash"],
                water=data["water"],
                superplasticizer=data["superplasticizer"],
                coarse_aggregate=data["coarse_aggregate"],
                fine_aggregate=data["fine_aggregate"],
                age=data["age"],
                predicted_strength=predicted_strength,
            )

            return redirect(
                "prediction:result",
                pk=prediction.pk
            )

    else:
        form = PredictionForm()

    return render(
        request,
        "prediction/predict.html",
        {"form": form}
    )


@login_required
def result_view(request, pk):
    prediction = get_object_or_404(
        Prediction,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "prediction/result.html",
        {"prediction": prediction}
    )

@login_required
def history_view(request):
    predictions = Prediction.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "prediction/history.html",
        {"predictions": predictions}
    )

@login_required
def analytics_view(request):
    predictions = Prediction.objects.filter(
        user=request.user
    ).order_by("created_at")

    stats = predictions.aggregate(
        average_strength=Avg("predicted_strength"),
        highest_strength=Max("predicted_strength"),
        lowest_strength=Min("predicted_strength"),
    )

    chart_labels = [
        prediction.created_at.strftime("%b %d, %Y")
        for prediction in predictions
    ]

    chart_values = [
        round(prediction.predicted_strength, 2)
        for prediction in predictions
    ]

    context = {
        "total_predictions": predictions.count(),
        "average_strength": stats["average_strength"],
        "highest_strength": stats["highest_strength"],
        "lowest_strength": stats["lowest_strength"],
        "chart_labels": chart_labels,
        "chart_values": chart_values,
    }

    return render(
        request,
        "prediction/analytics.html",
        context
    )

@login_required
@require_POST
def delete_view(request, pk):
    prediction = get_object_or_404(
        Prediction,
        pk=pk,
        user=request.user,
    )
    prediction.delete()
    messages.success(request, "Prediction deleted successfully.")
    return redirect("prediction:history")
