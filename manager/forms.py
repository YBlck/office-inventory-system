from django import forms
from django.contrib.auth.forms import UserCreationForm

from manager.models import Staff


class StaffForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Staff
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ("role", "email", "first_name", "last_name")