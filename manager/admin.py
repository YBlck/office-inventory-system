from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from manager.models import Staff, Equipment, Category


admin.site.unregister(Group)


@admin.register(Staff)
class StaffAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("role",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("role",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "role",
                    )
                },
            ),
        )
    )
    search_fields = ("username",)
    list_filter = ("role",)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("category",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description",)
