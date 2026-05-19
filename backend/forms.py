from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


# --- Форма регистрации ---
class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(required=False, label="Телефон")
    role = forms.ChoiceField(
        choices=[("visitor", "Посетитель"), ("master", "Мастер"), ("admin", "Админ")],
        initial="visitor",
        label="Роль"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "phone", "role")


# --- Форма редактирования ---
class CustomUserChangeForm(UserChangeForm):
    phone = forms.CharField(required=False, label="Телефон")
    role = forms.ChoiceField(
        choices=[("visitor", "Посетитель"), ("master", "Мастер"), ("admin", "Админ")],
        label="Роль"
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone", "role")
