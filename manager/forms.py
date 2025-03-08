from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from manager.models import Staff, Equipment


class StaffForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Staff
        fields = UserCreationForm.Meta.fields + (
            "email", "first_name", "last_name"
        )


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ("role", "email", "first_name", "last_name")


class EquipmentForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Equipment
        fields = "__all__"
