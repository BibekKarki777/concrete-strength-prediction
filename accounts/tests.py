from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from prediction.models import Prediction


class WorkspaceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("engineer", "engineer@example.com", "Existing-Password-42", first_name="Asha", last_name="Sharma")
        cls.admin = User.objects.create_user("manager", "manager@example.com", "Existing-Password-42", is_staff=True)
        cls.prediction = Prediction.objects.create(user=cls.user, cement=300, blast_furnace_slag=0, fly_ash=0, water=180, superplasticizer=5, coarse_aggregate=1000, fine_aggregate=800, age=28, predicted_strength=35)

    def test_public_navigation(self):
        for route in ["core:home", "core:about", "accounts:login", "accounts:register"]:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertContains(response, 'id="public-links"')
                self.assertNotContains(response, 'id="dashboard-sidebar"')

    def test_user_workspace_and_prediction_pages(self):
        self.client.force_login(self.user)
        for route in ["accounts:dashboard", "accounts:profile", "prediction:predict", "prediction:history", "prediction:analytics"]:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertContains(response, 'id="dashboard-sidebar"')
                self.assertContains(response, "Asha Sharma")
                self.assertContains(response, "<small>User</small>", html=True)
                self.assertNotContains(response, "Admin overview")
        self.assertEqual(self.client.get(reverse("prediction:result", args=[self.prediction.pk])).status_code, 200)

    def test_staff_landing_and_admin_pages(self):
        self.client.force_login(self.admin)
        self.assertRedirects(self.client.get(reverse("accounts:dashboard")), reverse("admin_dashboard:dashboard"))
        for route in ["admin_dashboard:dashboard", "admin_dashboard:users", "admin_dashboard:predictions", "admin_dashboard:model_info"]:
            with self.subTest(route=route):
                response = self.client.get(reverse(route))
                self.assertContains(response, "Admin overview")
                self.assertContains(response, "<small>Admin</small>", html=True)
        self.assertEqual(self.client.get(reverse("admin_dashboard:prediction_detail", args=[self.prediction.pk])).status_code, 200)

    def test_logout_returns_public_home_for_both_roles(self):
        for user in [self.user, self.admin]:
            self.client.force_login(user)
            response = self.client.post(reverse("accounts:logout"), follow=True)
            self.assertRedirects(response, reverse("core:home"))
            self.assertContains(response, 'id="public-links"')
            self.assertNotContains(response, 'id="dashboard-sidebar"')

    def test_regular_user_cannot_access_admin(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("admin_dashboard:dashboard")).status_code, 302)
