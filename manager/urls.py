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
    EquipmentAssignmentView,
    delete_user_from_equipment,
    RepairRequestListView,
    RepairRequestDetailView,
    RepairRequestCreateView,
    RepairRequestUpdateView,
    RepairRequestDeleteView,
    RepairRequestUserCreateView, repair_request_update_status,
)

app_name = "manager"
urlpatterns = [
    path("", index, name="index"),
    path("staff/", StaffListView.as_view(), name="staff-list"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("staff/create/", StaffCreateView.as_view(), name="staff-create"),
    path(
        "staff/register/", StaffRegisterView.as_view(), name="staff-register"
    ),
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
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail"
    ),
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
        "equipment/<int:pk>/assign/",
        EquipmentAssignmentView.as_view(), name="equipment-assign"
    ),
    path(
        "equipment/<int:pk>/delete/",
        EquipmentDeleteView.as_view(), name="equipment-delete"
    ),
    path(
        "equipment/<int:equipment_pk>/delete-user/<int:user_id>/",
        delete_user_from_equipment, name="equipment-delete-user"
    ),
    path(
        "repair-request/",
        RepairRequestListView.as_view(),
        name="repair-request-list"
    ),
    path(
        "repair-request/<int:pk>/",
        RepairRequestDetailView.as_view(),
        name="repair-request-detail"
    ),
    path(
        "repair-request/create/",
        RepairRequestCreateView.as_view(),
        name="repair-request-create"
    ),
    path(
        "repair-request/<int:equipment_pk>/create/<int:user_id>/",
        RepairRequestUserCreateView.as_view(),
        name="repair-request-user-create"
    ),
    path(
        "repair-request/<int:pk>/update/",
        RepairRequestUpdateView.as_view(),
        name="repair-request-update"
    ),
    path(
        "repair-request/<int:pk>/update-status/",
        repair_request_update_status,
        name="repair-request-update-status"
    ),
    path(
        "repair-request/<int:pk>/delete/",
        RepairRequestDeleteView.as_view(),
        name="repair-request-delete"
    ),
]
