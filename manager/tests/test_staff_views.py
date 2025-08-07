from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

LOGIN_URL = reverse("login")
STAFF_REGISTRATION_URL = reverse("manager:staff-register")
STAFF_LIST_URL = reverse("manager:staff-list")
STAFF_CREATE_URL = reverse("manager:staff-create")


def get_staff_detail_url(staff_id):
    return reverse("manager:staff-detail", args=[staff_id])


def get_staff_update_url(staff_id):
    return reverse("manager:staff-update", args=[staff_id])


def get_staff_delete_url(staff_id):
    return reverse("manager:staff-delete", args=[staff_id])


def create_employee(username: str, role: str = "employee"):
    return get_user_model().objects.create_user(
        username=username,
        password="1qazcde3",
        email="email@example.com>",
        role=role,
    )


class PublicStaffViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_employee = get_user_model().objects.create(
            username="test_employee",
            password="1qazcde3",
            email="test_employee@mail.com",
            role="employee",
        )

    def test_staff_register_view(self):
        response = self.client.get(STAFF_REGISTRATION_URL)
        self.assertEqual(response.status_code, 200)

        payload = {
            "username": "test_username",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "email": "test_email@example.com",
        }

        self.client.post(STAFF_REGISTRATION_URL, data=payload)
        new_staff = get_user_model().objects.get(username=payload["username"])

        self.assertEqual(new_staff.username, payload["username"])
        self.assertEqual(new_staff.email, payload["email"])
        self.assertEqual(new_staff.role, "employee")

    def test_staff_list_login_required(self):
        response = self.client.get(STAFF_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_staff_list_redirect_to_login_page(self):
        response = self.client.get(STAFF_LIST_URL)
        self.assertRedirects(response, LOGIN_URL + "?next=/staff/")

    def test_staff_detail_login_required(self):
        response = self.client.get(get_staff_detail_url(self.test_employee.id))
        self.assertNotEqual(response.status_code, 200)

    def test_staff_detail_redirect_to_login_page(self):
        response = self.client.get(get_staff_detail_url(self.test_employee.id))
        self.assertRedirects(
            response, LOGIN_URL + f"?next=/staff/{self.test_employee.id}/"
        )

    def test_staff_update_login_required(self):
        response = self.client.get(get_staff_update_url(self.test_employee.id))
        self.assertNotEqual(response.status_code, 200)

    def test_staff_update_redirect_to_login_page(self):
        response = self.client.get(get_staff_update_url(self.test_employee.id))
        self.assertRedirects(
            response,
            LOGIN_URL + f"?next=/staff/{self.test_employee.id}/update/",
        )

    def test_staff_delete_login_required(self):
        response = self.client.get(get_staff_delete_url(self.test_employee.id))
        self.assertNotEqual(response.status_code, 204)

    def test_staff_delete_redirect_to_login_page(self):
        response = self.client.get(get_staff_delete_url(self.test_employee.id))
        self.assertRedirects(
            response,
            LOGIN_URL + f"?next=/staff/{self.test_employee.id}/delete/",
        )

    def test_staff_create_login_required(self):
        response = self.client.get(STAFF_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_staff_create_redirect_to_login_page(self):
        response = self.client.get(STAFF_CREATE_URL)
        self.assertRedirects(response, LOGIN_URL + f"?next=/staff/create/")


class EmployeeStaffViewsTest(TestCase):
    def setUp(self):
        self.employee = create_employee("employee")
        self.client.force_login(self.employee)

    def test_staff_list_access(self):
        response = self.client.get(STAFF_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/staff_list.html")
        self.assertContains(response, self.employee.username)

    def test_staff_detail_own_profile_access(self):
        response = self.client.get(get_staff_detail_url(self.employee.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/staff_detail.html")
        self.assertContains(response, self.employee.username)

    def test_staff_detail_other_employee_profile_access(self):
        other_user = create_employee("other_test_user")
        response = self.client.get(get_staff_detail_url(other_user.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, other_user.username)

    def test_staff_create_employee_access_forbidden(self):
        response = self.client.get(STAFF_CREATE_URL)
        self.assertEqual(response.status_code, 403)

    def test_staff_update_own_profile_access(self):
        response = self.client.get(get_staff_update_url(self.employee.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/staff_form.html")
        self.assertContains(response, self.employee.username)

        payload = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "new_email@example.com",
            "role": "employee",
        }

        self.client.post(get_staff_update_url(self.employee.id), data=payload)
        updated_employee = get_user_model().objects.get(id=self.employee.id)

        self.assertEqual(updated_employee.first_name, payload["first_name"])
        self.assertEqual(updated_employee.last_name, payload["last_name"])
        self.assertEqual(updated_employee.email, payload["email"])

    def test_staff_update_other_employee_profile_access(self):
        other_user = create_employee("other_test_user")
        response = self.client.get(get_staff_update_url(other_user.id))
        self.assertEqual(response.status_code, 403)

    def test_staff_delete_own_profile_access(self):
        response = self.client.get(get_staff_delete_url(self.employee.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/staff_confirm_delete.html")

    def test_staff_delete_other_employee_profile_access(self):
        other_user = create_employee("other_test_user")
        response = self.client.get(get_staff_delete_url(other_user.id))
        self.assertEqual(response.status_code, 403)


class SupportStaffViewsTest(TestCase):
    def setUp(self):
        self.support = create_employee("test_support", "support")
        self.client.force_login(self.support)

    def test_staff_update_other_employee_profile_access(self):
        other_user = create_employee("other_test_user")
        response = self.client.get(get_staff_update_url(other_user.id))
        self.assertEqual(response.status_code, 403)

    def test_staff_delete_other_user_profile_access(self):
        other_user = create_employee("other_test_user")
        response = self.client.get(get_staff_delete_url(other_user.id))
        self.assertEqual(response.status_code, 403)

    def test_staff_create_employee_access(self):
        response = self.client.get(STAFF_CREATE_URL)
        self.assertEqual(response.status_code, 403)


class AdminStaffViewsTest(TestCase):
    def setUp(self):
        self.admin = create_employee("test_admin", "admin")
        self.client.force_login(self.admin)

    def test_staff_update_other_user_profile_access(self):
        other_user = create_employee("other_test_user")
        response = self.client.get(get_staff_update_url(other_user.id))
        self.assertEqual(response.status_code, 200)

        payload = {
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "email": "new_email@example.com",
            "role": "employee",
        }

        self.client.post(get_staff_update_url(other_user.id), data=payload)
        updated_employee = get_user_model().objects.get(id=other_user.id)

        self.assertEqual(updated_employee.first_name, payload["first_name"])
        self.assertEqual(updated_employee.last_name, payload["last_name"])
        self.assertEqual(updated_employee.email, payload["email"])

    def test_staff_delete_other_user_profile_access(self):
        other_user = create_employee("other_test_user")
        response = self.client.get(get_staff_delete_url(other_user.id))
        self.assertEqual(response.status_code, 200)

    def test_staff_create_employee_access(self):
        response = self.client.get(STAFF_CREATE_URL)
        self.assertEqual(response.status_code, 200)

        payload = {
            "username": "test_employee",
            "email": "test@example.com",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
        }
        self.client.post(STAFF_CREATE_URL, data=payload)
        new_employee = get_user_model().objects.get(
            username=payload["username"]
        )

        self.assertEqual(new_employee.username, payload["username"])
        self.assertEqual(new_employee.email, payload["email"])
