from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from manager.models import Staff, Equipment, EquipmentEmployeeAssignment


class StaffForm(UserCreationForm):
    email = forms.EmailField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = Staff
        fields = UserCreationForm.Meta.fields + (
            "email",
        )
        help_texts = {
            "username": None,
        }


class StaffUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = Staff
        fields = ("role", "email", "first_name", "last_name")


class StaffUsernameSearchForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control", "placeholder": "Search by username"
            }
        ),
    )


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = (
            "name",
            "category",
            "internal_serial_number",
            "manufacturer_serial_number"
        )

    def clean_internal_serial_number(self):
        serial_number = self.cleaned_data["internal_serial_number"]
        return validate_serial_number(serial_number)


class EquipmentAssignForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=get_user_model().objects.none(),
        required=False,
        label="Chose employee to assign:",
    )

    class Meta:
        model = Equipment
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            assigned_users = EquipmentEmployeeAssignment.objects.filter(
                equipment=self.instance
            ).values_list("employee_id", flat=True)

            self.fields[
                "assigned_to"
            ].queryset = get_user_model().objects.exclude(
                id__in=assigned_users
            )

    def save(self, commit=True):
        equipment = self.instance
        selected_employee = self.cleaned_data.get("assigned_to")

        if commit and selected_employee:
            EquipmentEmployeeAssignment.objects.get_or_create(
                equipment=equipment, employee=selected_employee
            )

        return equipment


# validation for internal serial number of equipment
def validate_serial_number(serial_number):
    if len(serial_number) != 10:
        raise ValidationError("Serial number should consist of 10 characters")
    elif not serial_number[:3].isupper() or not serial_number[:3].isalpha():
        raise ValidationError("First 3 characters should be uppercase letters")
    elif not serial_number[3:].isdigit():
        raise ValidationError("Last 7 characters should be digits")

    return serial_number


class EquipmentNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by name"}
        ),
    )


class CategoryNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by name"}
        ),
    )
