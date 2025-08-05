from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Category, Equipment, RepairRequest

LOGIN_URL = reverse("login")
REQUEST_LIST_URL = reverse("manager:repair-request-list")
REQUEST_CREATE_URL = reverse("manager:repair-request-create")


def get_request_detail_url(request_id):
    return reverse("manager:repair-request-detail", args=[request_id])


def get_request_update_url(request_id):
    return reverse("manager:repair-request-update", args=[request_id])


def get_request_delete_url(request_id):
    return reverse("manager:repair-request-delete", args=[request_id])


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


class PublicRepairRequestViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_category = create_category()
        cls.test_equipment = Equipment.objects.create(
            name="Test Equipment",
            category=cls.test_category,
            internal_serial_number="ABC1234567",
        )
        cls.test_employee = create_employee("test_employee")
        cls.test_repair_request = RepairRequest.objects.create(
            equipment=cls.test_equipment,
            employee=cls.test_employee,
            description="Test Repair Request",
        )

    def test_request_list_login_required(self):
        response = self.client.get(REQUEST_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_request_list_redirect_to_login_page(self):
        response = self.client.get(REQUEST_LIST_URL)
        self.assertRedirects(response, LOGIN_URL + "?next=/repair-requests/")

    def test_request_detail_login_required(self):
        response = self.client.get(
            get_request_detail_url(self.test_repair_request.id)
        )
        self.assertNotEqual(response.status_code, 200)

    def test_request_detail_redirect_to_login_page(self):
        response = self.client.get(
            get_request_detail_url(self.test_repair_request.id)
        )
        self.assertRedirects(
            response,
            LOGIN_URL
            + f"?next=/repair-requests/{self.test_repair_request.id}/",
        )

    def test_request_update_login_required(self):
        response = self.client.get(
            get_request_update_url(self.test_repair_request.id)
        )
        self.assertNotEqual(response.status_code, 200)

    def test_request_update_redirect_to_login_page(self):
        response = self.client.get(
            get_request_update_url(self.test_repair_request.id)
        )
        self.assertRedirects(
            response,
            LOGIN_URL
            + f"?next=/repair-requests/{self.test_repair_request.id}/update/",
        )

    def test_request_delete_login_required(self):
        response = self.client.get(
            get_request_delete_url(self.test_repair_request.id)
        )
        self.assertNotEqual(response.status_code, 204)

    def test_request_delete_redirect_to_login_page(self):
        response = self.client.get(
            get_request_delete_url(self.test_repair_request.id)
        )
        self.assertRedirects(
            response,
            LOGIN_URL
            + f"?next=/repair-requests/{self.test_repair_request.id}/delete/",
        )

    def test_request_create_login_required(self):
        response = self.client.get(REQUEST_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_request_create_redirect_to_login_page(self):
        response = self.client.get(REQUEST_CREATE_URL)
        self.assertRedirects(
            response, LOGIN_URL + f"?next=/repair-requests/create/"
        )


class EmployeeRepairRequestViewsTest(TestCase):
    def setUp(self):
        self.test_employee = create_employee("test_employee")
        self.client.force_login(self.test_employee)
        self.test_category = create_category()
        self.test_equipment = Equipment.objects.create(
            name="Test Equipment 0",
            category=self.test_category,
            internal_serial_number="ABC1234567",
        )
        self.test_equipment.assigned_to.set([self.test_employee])
        self.test_repair_request = RepairRequest.objects.create(
            equipment=self.test_equipment,
            employee=self.test_employee,
            description="Test Repair Request",
        )

    def test_request_list(self):
        for i in range(1, 3):
            Equipment.objects.create(
                name=f"Test Equipment {i}",
                category=self.test_category,
                internal_serial_number=f"ABC000000{i}",
            )

        equipment = Equipment.objects.all()

        for i, element in enumerate(equipment):
            RepairRequest.objects.create(
                equipment=element,
                employee=self.test_employee,
                description=f"Test Repair Request {i}",
            )

        response = self.client.get(REQUEST_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/repair_request_list.html")

        requests = RepairRequest.objects.all()
        for request in requests:
            self.assertContains(response, request.equipment.name)

    def test_request_create_access(self):
        response = self.client.get(REQUEST_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/repair_request_form.html")

    def test_request_detail_access(self):
        response = self.client.get(
            get_request_detail_url(self.test_repair_request.id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/repair_request_detail.html")

    def test_request_update_request_access(self):
        response = self.client.get(
            get_request_update_url(self.test_repair_request.id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/repair_request_form.html")

    def test_request_delete_access(self):
        response = self.client.get(
            get_request_delete_url(self.test_repair_request.id)
        )
        self.assertEqual(response.status_code, 403)


class SupportRepairRequestViewsTest(TestCase):
    def setUp(self):
        self.test_employee = create_employee("test_employee", "support")
        self.client.force_login(self.test_employee)
        self.test_category = create_category()
        self.test_equipment = Equipment.objects.create(
            name="Test Equipment 0",
            category=self.test_category,
            internal_serial_number="ABC1234567",
        )
        self.test_equipment.assigned_to.set([self.test_employee])
        self.test_repair_request = RepairRequest.objects.create(
            equipment=self.test_equipment,
            employee=self.test_employee,
            description="Test Repair Request",
        )

    def test_request_delete_access(self):
        response = self.client.get(
            get_request_delete_url(self.test_repair_request.id)
        )
        self.assertEqual(response.status_code, 200)
