from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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

    def get_absolute_url(self):
        return reverse("manager:staff-detail", kwargs={"pk": self.pk})

    def get_role_display(self):
        return dict(Staff.ROLE_CHOICES)[self.role]


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
    manufacturer_serial_number = models.CharField(max_length=100, blank=True, null=True)
    internal_serial_number = models.CharField(max_length=10, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="EquipmentEmployeeAssignment",
        blank=True,
        related_name="assigned_equipment",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

    def __str__(self):
        return f"{self.name} - {self.internal_serial_number} ({self.category})"

    def get_absolute_url(self):
        return reverse("manager:equipment-detail", kwargs={"pk": self.pk})


class EquipmentEmployeeAssignment(models.Model):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="assignments"
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employees",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["employee"]


class RepairRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="repair_requests")
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="repair_requests"
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    description = models.TextField(blank=True, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-date_reported"]

    def __str__(self):
        return f"{self.equipment} - {self.employee}"

    def get_absolute_url(self):
        return reverse("manager:repair-request-detail", kwargs={"pk": self.pk})

    def get_status_display(self):
        return dict(RepairRequest.STATUS_CHOICES)[self.status]
