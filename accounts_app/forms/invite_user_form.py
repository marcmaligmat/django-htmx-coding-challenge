from django import forms


class InviteUserForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control w-full',
        'placeholder': 'Enter email',
    }))
