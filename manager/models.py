from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Staff(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("employee", "Employee"),
        ("support", "Support"),
    ]
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default="employee",
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "Staff member"
        verbose_name_plural = "Staff members"

    def __str__(self):
        return f"{self.username} ({self.role})"


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="equipment",
    )
    manufacturer_serial_number = models.CharField(
        max_length=100, blank=True, null=True
    )
    internal_serial_number = models.CharField(max_length=10, unique=True)
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="EquipmentEmployeeAssignment",
        blank=True,
        related_name="employees",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

    def __str__(self):
        return f"{self.name} - {self.internal_serial_number} ({self.category})"


class EquipmentEmployeeAssignment(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["employee"]
