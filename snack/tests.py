from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class ThingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin1", email="admin1@email.com", password="pass"
        )

        self.snack = Snack.objects.create(
            title="cheese", description="good", purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "cheese")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "cheese")
        self.assertEqual(f"{self.snack.purchaser}", "admin1")
        self.assertEqual(f"{self.snack.description}", "good")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snacks_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cheese")
        self.assertTemplateUsed(response, "snack/snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "purchaser: admin1")
        self.assertTemplateUsed(response, "snack/snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "admin2",
                "description": "wow",
                "purchaser": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Details about admin2")



    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Updated name","description":"3","purchaser":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)