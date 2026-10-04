from django.contrib.auth.models import User
from django.db import models


class Prediction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="predictions"
    )

    cement = models.FloatField()
    blast_furnace_slag = models.FloatField()
    fly_ash = models.FloatField()
    water = models.FloatField()
    superplasticizer = models.FloatField()
    coarse_aggregate = models.FloatField()
    fine_aggregate = models.FloatField()
    age = models.PositiveIntegerField()

    predicted_strength = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_strength:.2f} MPa"