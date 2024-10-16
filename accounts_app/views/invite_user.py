from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts_app.forms import InviteUserForm
from accounts_app.models import UserInvitation
from django.contrib import messages


class InviteUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = InviteUserForm()
        return render(request, "accounts_app/invite_modal.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = InviteUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            UserInvitation.objects.filter(
                email=email).delete()

            invitation = UserInvitation(
                email=email, invited_by=request.user)
            invitation.save()

            invitation.send_invitation_email()
            messages.success(
                request, f"An invitation email has been sent to {email}.")

            return render(request, "accounts_app/profile.html", {"invite_user_form": form, "invited": True})
        else:
            return render(request, "accounts_app/profile.html", {"invite_user_form": form})
