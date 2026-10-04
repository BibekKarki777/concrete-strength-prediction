from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class HomeRoutingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="home_user")
        cls.admin = User.objects.create_user(
            username="home_admin",
            is_staff=True,
        )

    def test_visitor_sees_public_home(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertContains(response, 'id="public-links"')

    def test_user_goes_to_personal_dashboard(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("core:home"), follow=True)
        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertTemplateUsed(response, "accounts/dashboard.html")
        self.assertTemplateNotUsed(response, "core/home.html")

    def test_admin_goes_to_admin_dashboard(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("core:home"), follow=True)
        self.assertRedirects(response, reverse("admin_dashboard:dashboard"))
        self.assertTemplateUsed(response, "admin_dashboard/dashboard.html")
        self.assertTemplateNotUsed(response, "core/home.html")

    def test_logout_restores_public_home(self):
        for user in [self.user, self.admin]:
            with self.subTest(user=user.username):
                self.client.force_login(user)
                response = self.client.post(reverse("accounts:logout"), follow=True)
                self.assertRedirects(response, reverse("core:home"))
                self.assertTemplateUsed(response, "core/home.html")
