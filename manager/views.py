from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import (
    StaffForm,
    StaffUpdateForm,
    EquipmentForm,
    StaffUsernameSearchForm,
    CategoryNameSearchForm,
    EquipmentNameSearchForm,
    EquipmentAssignForm,
)
from manager.models import Staff, Equipment, Category


def index(request):
    """View function for the home page of the site."""

    num_staff = Staff.objects.count()
    num_equipment = Equipment.objects.count()
    num_categories = Category.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_staff": num_staff,
        "num_equipment": num_equipment,
        "num_categories": num_categories,
        "num_visits": num_visits + 1,
    }

    return render(request, "manager/index.html", context=context)


class StaffListView(generic.ListView):
    model = Staff
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StaffListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")

        context["search_form"] = StaffUsernameSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = StaffUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"].strip()
            )
        return queryset


class StaffDetailView(generic.DetailView):
    model = Staff
    queryset = Staff.objects.prefetch_related(
        "assigned_equipment__assignments__employee"
    ).prefetch_related(
        "assigned_equipment__category"
    )


class StaffCreateView(generic.CreateView):
    model = Staff
    form_class = StaffForm


class StaffRegisterView(generic.CreateView):
    model = Staff
    form_class = StaffForm
    template_name = "registration/register.html"


class StaffUpdateView(generic.UpdateView):
    model = Staff
    form_class = StaffUpdateForm


class StaffDeleteView(generic.DeleteView):
    model = Staff
    success_url = reverse_lazy("manager:staff-list")


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = CategoryNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CategoryNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"].strip()
            )
        return queryset


class CategoryCreateView(generic.CreateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("manager:category-list")


class CategoryDetailView(generic.DetailView):
    model = Category


class CategoryUpdateView(generic.UpdateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("manager:category-list")


class CategoryDeleteView(generic.DeleteView):
    model = Category
    success_url = reverse_lazy("manager:category-list")


class EquipmentListView(generic.ListView):
    model = Equipment
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EquipmentListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = EquipmentNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Equipment.objects.select_related("category")
        form = EquipmentNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"].strip()
            )
        return queryset


class EquipmentDetailView(generic.DetailView):
    model = Equipment


class EquipmentCreateView(generic.CreateView):
    model = Equipment
    form_class = EquipmentForm


class EquipmentAssignmentView(generic.UpdateView):
    model = Equipment
    form_class = EquipmentAssignForm
    template_name = "manager/equipment_assign.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment = self.get_object()
        added_users = self.request.session.get(f"added_users_{equipment.pk}", [])
        context["added_users"] = get_user_model().objects.filter(id__in=added_users)
        return context

    def form_valid(self, form):
        equipment = self.get_object()
        added_users = self.request.session.get(f"added_users_{equipment.pk}", [])

        if form.cleaned_data["assigned_to"]:
            user_id = form.cleaned_data["assigned_to"].id
            if user_id not in added_users:
                added_users.append(user_id)

        self.request.session[f"added_users_{equipment.pk}"] = added_users
        equipment.assigned_to.set(get_user_model().objects.filter(id__in=added_users))
        return redirect("manager:equipment-detail", pk=equipment.pk)


def delete_user_from_equipment(request, equipment_pk, user_id):
    equipment = get_object_or_404(Equipment, pk=equipment_pk)
    user = get_object_or_404(get_user_model(), pk=user_id)

    if user in equipment.assigned_to.all():
        equipment.assigned_to.remove(user)

    return redirect("manager:equipment-detail", pk=equipment_pk)


class EquipmentUpdateView(generic.UpdateView):
    model = Equipment
    form_class = EquipmentForm


class EquipmentDeleteView(generic.DeleteView):
    model = Equipment
    success_url = reverse_lazy("manager:equipment-list")
