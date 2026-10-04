from django.test import TestCase

# Create your tests here.


from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from .models import Prediction


class DeletePredictionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner")
        self.other = User.objects.create_user(username="other")
        self.prediction = Prediction.objects.create(
            user=self.owner,
            cement=300,
            blast_furnace_slag=0,
            fly_ash=0,
            water=180,
            superplasticizer=5,
            coarse_aggregate=1000,
            fine_aggregate=800,
            age=28,
            predicted_strength=35,
        )
        self.url = reverse("prediction:delete", args=[self.prediction.pk])

    def test_owner_can_delete_with_post(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse("prediction:history"))
        self.assertFalse(Prediction.objects.filter(pk=self.prediction.pk).exists())
        self.assertContains(response, "Prediction deleted successfully.")

    def test_another_user_cannot_delete(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.post(self.url).status_code, 404)
        self.assertTrue(Prediction.objects.filter(pk=self.prediction.pk).exists())

    def test_get_and_anonymous_requests_do_not_delete(self):
        self.assertEqual(self.client.post(self.url).status_code, 302)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.assertTrue(Prediction.objects.filter(pk=self.prediction.pk).exists())

    def test_csrf_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        self.assertEqual(client.post(self.url).status_code, 403)
        self.assertTrue(Prediction.objects.filter(pk=self.prediction.pk).exists())
