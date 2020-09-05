from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Conferma password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Password'}),
    )
    first_name = forms.CharField(
        label="Nome",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nome'}
        ),
        max_length=30,
        required=False,
        help_text='Opzionale.')
    last_name = forms.CharField(
        label="Cognome",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Cognome'}
        ),
        max_length=30,
        required=False,
        help_text='Opzionale.')
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
        ),
        max_length=254,
        help_text='Obbligatorio, inserisci un indirizzo email valido.')
    CHOICES = [(group.name, group.name) for group in Group.objects.all()]
    groups = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.widgets.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'groups', )

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cognome'}),
        }