from django.test import TestCase
from django.urls import reverse

from accounts_app.models import User


class TestProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="John",
            last_name="Doe",
        )
        self.client.force_login(self.user)

    def test_get(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context["user"].first_name, "John")
        self.assertEqual(context["user"].last_name, "Doe")

    def test_post(self):
        response = self.client.post(
            reverse("home"),
            {
                "first_name": "Jane",
                "last_name": "Sample",
            },
        )

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context["user"].first_name, "Jane")
        self.assertEqual(context["user"].last_name, "Sample")

        # validate no errors in form
        self.assertFalse(context["form"].errors)

    def test_post_valid_data(self):
        response = self.client.post(
            reverse("home"),
            {
                "first_name": "Jane",
                "last_name": "Sample",
                "occupation": "Developer",  # Include occupation for valid case
            },
        )

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context["user"].first_name, "Jane")
        self.assertEqual(context["user"].last_name, "Sample")
        # Check occupation is updated
        self.assertEqual(context["user"].occupation, "Developer")

        # Validate no errors in form
        self.assertFalse(context["form"].errors)

    def test_post_valid_data_without_occupation(self):
        response = self.client.post(
            reverse("home"),
            {
                "first_name": "Jane",
                "last_name": "Sample",
                # Occupation is omitted
            },
        )

        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertEqual(context["user"].first_name, "Jane")
        self.assertEqual(context["user"].last_name, "Sample")
        # Check occupation is not set
        self.assertIsNone(context["user"].occupation)

        # Validate no errors in form
        self.assertFalse(context["form"].errors)

    def test_post_invalid_data(self):
        response = self.client.post(
            reverse("home"),
            {
                "first_name": "",  # Invalid first name
                "last_name": "Sample",
                "occupation": "Developer",
            },
        )

        self.assertEqual(response.status_code, 200)
        context = response.context

        # Validate that form has errors
        self.assertTrue(context["form"].errors)
        # Check for specific error
        self.assertIn('first_name', context["form"].errors)

    def test_post_partial_update(self):
        response = self.client.post(
            reverse("home"),
            {
                "first_name": "John",  # Keeping the same name
                "last_name": "Smith",  # Updating last name
                "occupation": "Senior Engineer",  # Updating occupation
            },
        )

        self.assertEqual(response.status_code, 200)

        context = response.context
        # First name remains unchanged
        self.assertEqual(context["user"].first_name, "John")
        self.assertEqual(context["user"].last_name,
                         "Smith")  # Last name updated
        self.assertEqual(context["user"].occupation,
                         "Senior Engineer")  # Occupation updated

        # Validate no errors in form
        self.assertFalse(context["form"].errors)

    def test_post_invalid_last_name(self):
        response = self.client.post(
            reverse("home"),
            {
                "first_name": "Jane",
                "last_name": "",  # Invalid last name
                "occupation": "Developer",
            },
        )

        self.assertEqual(response.status_code, 200)
        context = response.context

        # Validate that form has errors
        self.assertTrue(context["form"].errors)
        self.assertIn('last_name', context["form"].errors)
