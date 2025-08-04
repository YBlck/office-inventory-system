from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Category, Equipment

LOGIN_URL = reverse("login")
EQUIPMENT_LIST_URL = reverse("manager:equipment-list")
EQUIPMENT_CREATE_URL = reverse("manager:equipment-create")


def get_equipment_detail_url(equipment_id):
    return reverse("manager:equipment-detail", args=[equipment_id])


def get_equipment_update_url(equipment_id):
    return reverse("manager:equipment-update", args=[equipment_id])


def get_equipment_delete_url(equipment_id):
    return reverse("manager:equipment-delete", args=[equipment_id])


def create_employee(username: str, role: str = "employee"):
    return get_user_model().objects.create_user(
        username=username,
        password="1qazcde3",
        email="email@example.com>",
        role=role,
    )


def create_category(name: str = "test_category"):
    return Category.objects.create(
        name=name,
        description="Test category description",
    )


class PublicEquipmentViewsTest(TestCase):
    def setUp(self):
        self.test_category = create_category()
        self.test_equipment = Equipment.objects.create(
            name="Test Equipment",
            category=self.test_category,
            internal_serial_number="ABC1234567",
        )

    def test_equipment_list_login_required(self):
        response = self.client.get(EQUIPMENT_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_equipment_list_redirect_to_login_page(self):
        response = self.client.get(EQUIPMENT_LIST_URL)
        self.assertRedirects(response, LOGIN_URL + "?next=/equipment/")

    def test_equipment_detail_login_required(self):
        response = self.client.get(
            get_equipment_detail_url(self.test_category.id)
        )
        self.assertNotEqual(response.status_code, 200)

    def test_equipment_detail_redirect_to_login_page(self):
        response = self.client.get(
            get_equipment_detail_url(self.test_category.id)
        )
        self.assertRedirects(
            response, LOGIN_URL + f"?next=/equipment/{self.test_equipment.id}/"
        )

    def test_equipment_update_login_required(self):
        response = self.client.get(
            get_equipment_update_url(self.test_equipment.id)
        )
        self.assertNotEqual(response.status_code, 200)

    def test_equipment_update_redirect_to_login_page(self):
        response = self.client.get(
            get_equipment_update_url(self.test_equipment.id)
        )
        self.assertRedirects(
            response,
            LOGIN_URL + f"?next=/equipment/{self.test_equipment.id}/update/",
        )

    def test_equipment_delete_login_required(self):
        response = self.client.get(
            get_equipment_delete_url(self.test_equipment.id)
        )
        self.assertNotEqual(response.status_code, 204)

    def test_equipment_delete_redirect_to_login_page(self):
        response = self.client.get(
            get_equipment_delete_url(self.test_equipment.id)
        )
        self.assertRedirects(
            response,
            LOGIN_URL + f"?next=/equipment/{self.test_equipment.id}/delete/",
        )

    def test_equipment_create_login_required(self):
        response = self.client.get(EQUIPMENT_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_equipment_create_redirect_to_login_page(self):
        response = self.client.get(EQUIPMENT_CREATE_URL)
        self.assertRedirects(response, LOGIN_URL + f"?next=/equipment/create/")


class EmployeeEquipmentViewsTest(TestCase):
    def setUp(self):
        self.test_category = create_category()
        self.test_equipment = Equipment.objects.create(
            name="Test Equipment",
            category=self.test_category,
            internal_serial_number="ABC1234567",
        )
        self.test_employee = create_employee("test_employee")
        self.client.force_login(self.test_employee)

    def test_equipment_list(self):
        for i in range(1, 3):
            Equipment.objects.create(
                name=f"test_equipment_{i}",
                category=self.test_category,
                internal_serial_number=f"ABC000000{i}",
            )

        response = self.client.get(EQUIPMENT_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/equipment_list.html")
        equipment = Category.objects.all()

        for element in equipment:
            self.assertContains(response, element.name)

    def test_equipment_create_access(self):
        response = self.client.get(EQUIPMENT_CREATE_URL)
        self.assertEqual(response.status_code, 403)

    def test_equipment_update_access(self):
        response = self.client.get(
            get_equipment_update_url(self.test_equipment.id)
        )
        self.assertEqual(response.status_code, 403)

    def test_equipment_delete_access(self):
        response = self.client.get(
            get_equipment_delete_url(self.test_equipment.id)
        )
        self.assertEqual(response.status_code, 403)


class SupportEquipmentViewsTest(TestCase):
    def setUp(self):
        self.test_category = create_category()
        self.test_equipment = Equipment.objects.create(
            name="Test Equipment",
            category=self.test_category,
            internal_serial_number="ABC1234567",
        )
        self.test_support = create_employee("test_support", "support")
        self.client.force_login(self.test_support)

    def test_equipment_create_access(self):
        response = self.client.get(EQUIPMENT_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/equipment_form.html")

    def test_equipment_update_access(self):
        response = self.client.get(
            get_equipment_update_url(self.test_equipment.id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/equipment_form.html")

    def test_equipment_delete_access(self):
        response = self.client.get(
            get_equipment_delete_url(self.test_equipment.id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "manager/equipment_confirm_delete.html"
        )


class AdminEquipmentViewsTest(TestCase):
    def setUp(self):
        self.test_category = create_category()
        self.test_equipment = Equipment.objects.create(
            name="Test Equipment",
            category=self.test_category,
            internal_serial_number="ABC1234567",
        )
        self.test_admin = create_employee("test_admin", "admin")
        self.client.force_login(self.test_admin)

    def test_equipment_create_access(self):
        response = self.client.get(EQUIPMENT_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/equipment_form.html")

    def test_equipment_update_access(self):
        response = self.client.get(
            get_equipment_update_url(self.test_equipment.id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/equipment_form.html")

    def test_equipment_delete_access(self):
        response = self.client.get(
            get_equipment_delete_url(self.test_equipment.id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "manager/equipment_confirm_delete.html"
        )
