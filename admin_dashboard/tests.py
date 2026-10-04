from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from prediction.models import Prediction


class AdminPredictionDeletionTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(username="staff", is_staff=True)
        self.owner = User.objects.create_user(username="owner")
        self.record = Prediction.objects.create(
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
        self.url = reverse("admin_dashboard:delete_prediction", args=[self.record.pk])

    def test_staff_can_delete_another_users_prediction(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("admin_dashboard:predictions"))
        self.assertFalse(Prediction.objects.filter(pk=self.record.pk).exists())

    def test_dashboard_delete_returns_to_dashboard(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url, {"return_to": "dashboard"})
        self.assertRedirects(response, reverse("admin_dashboard:dashboard"))

    def test_untrusted_redirect_is_ignored(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url, {"return_to": "https://example.com"})
        self.assertRedirects(response, reverse("admin_dashboard:predictions"))

    def test_regular_user_and_anonymous_cannot_delete(self):
        self.assertEqual(self.client.post(self.url).status_code, 302)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(self.url).status_code, 302)
        self.assertTrue(Prediction.objects.filter(pk=self.record.pk).exists())

    def test_get_and_missing_csrf_do_not_delete(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(self.url).status_code, 405)
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.staff)
        self.assertEqual(client.post(self.url).status_code, 403)
        self.assertTrue(Prediction.objects.filter(pk=self.record.pk).exists())

    def test_admin_tables_render_actions_and_numeric_ids(self):
        self.client.force_login(self.staff)
        for route in ["admin_dashboard:dashboard", "admin_dashboard:predictions"]:
            response = self.client.get(reverse(route))
            self.assertContains(response, self.url)
            self.assertContains(response, "data-confirm-delete")
            self.assertContains(response, "admin-value-badge")
            self.assertNotContains(response, "#" + str(self.record.pk) + "</td>")
        response = self.client.get(reverse("admin_dashboard:users"))
        self.assertContains(response, "prediction-count admin-value-badge")
        self.assertContains(
            response,
            '<span class="prediction-count admin-value-badge">Staff</span>',
            html=True,
        )
