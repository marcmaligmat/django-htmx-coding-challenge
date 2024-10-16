from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts_app.models import UserInvitation
from accounts_app.forms import InviteUserForm

User = get_user_model()


class TestInviteUserView(TestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(
            email="test@test.com",
            password="test",
            first_name="John",
            last_name="Doe",
        )
        self.client.force_login(self.user)

    def test_get_invite_user_view(self):
        response = self.client.get(reverse("invite_user"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts_app/invite_modal.html")
        self.assertIsInstance(response.context['form'], InviteUserForm)

    def test_post_invite_user_view_success(self):
        response = self.client.post(reverse("invite_user"), {
            "email": "invitee@test.com"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts_app/profile.html")

        # Check if invitation was created
        invitation = UserInvitation.objects.filter(
            email="invitee@test.com").first()
        self.assertIsNotNone(invitation)
        self.assertEqual(invitation.invited_by, self.user)

        # Check for success message in response
        messages = list(response.wsgi_request._messages)
        self.assertEqual(
            str(messages[0]), "An invitation email has been sent to invitee@test.com.")

    def test_post_invite_user_view_invalid(self):
        # Test with an invalid email (if the form validation fails)
        response = self.client.post(reverse("invite_user"), {
            "email": ""  # Invalid email, assuming it's required
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts_app/profile.html")
        # Check for form errors
        self.assertTrue(response.context['invite_user_form'].errors)
