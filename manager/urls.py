from django.urls import path

from manager.views import (
    index,
    StaffListView,
    StaffDetailView,
    CategoryListView,
    EquipmentListView,
    EquipmentDetailView,
    StaffCreateView,
    StaffUpdateView,
    StaffDeleteView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    EquipmentCreateView,
    EquipmentUpdateView,
    EquipmentDeleteView,
    StaffRegisterView,
    CategoryDetailView,
)

app_name = "manager"
urlpatterns = [
    path("", index, name="index"),
    path("staff/", StaffListView.as_view(), name="staff-list"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("staff/create/", StaffCreateView.as_view(), name="staff-create"),
    path("staff/register/", StaffRegisterView.as_view(), name="staff-register"),
    path(
        "staff/<int:pk>/update/",
        StaffUpdateView.as_view(),
        name="staff-update"
    ),
    path(
        "staff/<int:pk>/delete/",
        StaffDeleteView.as_view(),
        name="staff-delete"
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path(
        "categories/create/",
        CategoryCreateView.as_view(),
        name="category-create"
    ),
    path(
        "categories/<int:pk>/update",
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    path(
        "categories/<int:pk>/delete",
        CategoryDeleteView.as_view(),
        name="category-delete"
    ),
    path("equipment/", EquipmentListView.as_view(), name="equipment-list"),
    path(
        "equipment/<int:pk>/",
        EquipmentDetailView.as_view(), name="equipment-detail"
    ),
    path(
        "equipment/create",
        EquipmentCreateView.as_view(),
        name="equipment-create"
    ),
    path(
        "equipment/<int:pk>/update/",
        EquipmentUpdateView.as_view(), name="equipment-update"
    ),
    path(
        "equipment/<int:pk>/delete/",
        EquipmentDeleteView.as_view(), name="equipment-delete"
    ),
]
