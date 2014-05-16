from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.PasswordInput()
    client_id = forms.HiddenInput()
    client_token = forms.HiddenInput()