from django import forms
from accounts_app.models import User


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "occupation"]

    occupation = forms.CharField(required=False)

    def save(self, commit=True):
        user = super().save(commit=False)  # Get the instance without saving

        # Set occupation to None if it's an empty string
        if self.cleaned_data.get("occupation") == '':
            user.occupation = None
        else:
            user.occupation = self.cleaned_data.get("occupation")

        if commit:
            user.save()  # Save the instance if commit is True

        return user
