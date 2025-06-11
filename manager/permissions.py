from django.contrib.auth.mixins import UserPassesTestMixin


class AdminPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "admin"


class AdminOrSelfPermissionMixin(AdminPermissionMixin):
    def test_func(self):
        if hasattr(self, "get_object"):
            if self.request.user == self.get_object():
                return True
        return super().test_func()


class SupportPermissionMixin(AdminPermissionMixin):
    def test_func(self):
        if self.request.user.role == "support":
            return True
        return super().test_func()
