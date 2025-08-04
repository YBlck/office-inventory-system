from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from manager.models import Category

LOGIN_URL = reverse("login")
CATEGORY_LIST_URL = reverse("manager:category-list")
CATEGORY_CREATE_URL = reverse("manager:category-create")


def get_category_detail_url(category_id):
    return reverse("manager:category-detail", args=[category_id])


def get_category_update_url(category_id):
    return reverse("manager:category-update", args=[category_id])


def get_category_delete_url(category_id):
    return reverse("manager:category-delete", args=[category_id])


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


class PublicCategoryViewsTest(TestCase):
    def setUp(self):
        self.test_category = create_category()

    def test_category_list_login_required(self):
        response = self.client.get(CATEGORY_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_category_list_redirect_to_login_page(self):
        response = self.client.get(CATEGORY_LIST_URL)
        self.assertRedirects(response, LOGIN_URL + "?next=/categories/")

    def test_category_detail_login_required(self):
        response = self.client.get(
            get_category_detail_url(self.test_category.id)
        )
        self.assertNotEqual(response.status_code, 200)

    def test_category_detail_redirect_to_login_page(self):
        response = self.client.get(
            get_category_detail_url(self.test_category.id)
        )
        self.assertRedirects(
            response, LOGIN_URL + f"?next=/categories/{self.test_category.id}/"
        )

    def test_category_update_login_required(self):
        response = self.client.get(
            get_category_update_url(self.test_category.id)
        )
        self.assertNotEqual(response.status_code, 200)

    def test_category_update_redirect_to_login_page(self):
        response = self.client.get(
            get_category_update_url(self.test_category.id)
        )
        self.assertRedirects(
            response,
            LOGIN_URL + f"?next=/categories/{self.test_category.id}/update/",
        )

    def test_category_delete_login_required(self):
        response = self.client.get(
            get_category_delete_url(self.test_category.id)
        )
        self.assertNotEqual(response.status_code, 204)

    def test_category_delete_redirect_to_login_page(self):
        response = self.client.get(
            get_category_delete_url(self.test_category.id)
        )
        self.assertRedirects(
            response,
            LOGIN_URL + f"?next=/categories/{self.test_category.id}/delete/",
        )

    def test_category_create_login_required(self):
        response = self.client.get(CATEGORY_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_category_create_redirect_to_login_page(self):
        response = self.client.get(CATEGORY_CREATE_URL)
        self.assertRedirects(
            response, LOGIN_URL + f"?next=/categories/create/"
        )


class EmployeeCategoryViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = create_employee("test_employee")
        self.client.force_login(self.test_user)
        self.test_category = create_category()

    def test_category_list(self):
        for i in range(1, 3):
            create_category(f"test_category_{i}")

        response = self.client.get(CATEGORY_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/category_list.html")
        categories = Category.objects.all()

        for category in categories:
            self.assertContains(response, category.name)

    def test_category_create_access(self):
        response = self.client.get(CATEGORY_CREATE_URL)
        self.assertEqual(response.status_code, 403)

    def test_category_update_access(self):
        response = self.client.get(
            get_category_update_url(self.test_category.id)
        )
        self.assertEqual(response.status_code, 403)

    def test_category_delete_access(self):
        response = self.client.get(
            get_category_delete_url(self.test_category.id)
        )
        self.assertEqual(response.status_code, 403)


class SupportCategoryViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = create_employee("test_support", role="support")
        self.client.force_login(self.test_user)
        self.test_category = create_category()

    def test_category_create_access(self):
        response = self.client.get(CATEGORY_CREATE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/category_form.html")

    def test_category_update_access(self):
        response = self.client.get(
            get_category_update_url(self.test_category.id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager/category_form.html")
        self.assertContains(response, self.test_category.name)

    def test_category_delete_access(self):
        response = self.client.get(
            get_category_delete_url(self.test_category.id)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "manager/category_confirm_delete.html"
        )
        self.assertContains(response, self.test_category.name)


class AdminCategoryViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = create_employee("test_admin", role="admin")
        self.client.force_login(self.test_user)
        self.test_category = create_category()

    def test_category_create_access(self):
        response = self.client.get(CATEGORY_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_category_update_access(self):
        response = self.client.get(
            get_category_update_url(self.test_category.id)
        )
        self.assertEqual(response.status_code, 200)

    def test_category_delete_access(self):
        response = self.client.get(
            get_category_delete_url(self.test_category.id)
        )
        self.assertEqual(response.status_code, 200)
