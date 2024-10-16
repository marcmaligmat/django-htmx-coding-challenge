from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts_app.forms import EditUserForm, InviteUserForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = EditUserForm(instance=request.user)
        invite_user_form = InviteUserForm()
        return render(request, "accounts_app/profile.html", {"form": form, "invite_user_form": invite_user_form})

    def post(self, request, *args, **kwargs):
        form = EditUserForm(request.POST, instance=request.user)
        invite_user_form = InviteUserForm()

        if form.is_valid():
            form.save()  # Just call save, which now handles occupation logic

        return render(request, "accounts_app/profile.html", {"form": form, "invite_user_form": invite_user_form})
