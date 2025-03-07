from django.urls import path

from manager.views import (
    index,
    StaffListView,
    StaffDetailView,
    CategoryListView,
    EquipmentListView,
    EquipmentDetailView,
)

app_name = "manager"
urlpatterns = [
    path("", index, name="index"),
    path("staff/", StaffListView.as_view(), name="staff-list"),
    path("staff/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("equipment/", EquipmentListView.as_view(), name="equipment-list"),
    path(
        "equipment/<int:pk>/",
        EquipmentDetailView.as_view(), name="equipment-detail"
    ),
]
