from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from manager.forms import (
    StaffForm,
    StaffUpdateForm,
    EquipmentForm,
    StaffUsernameSearchForm,
    CategoryNameSearchForm,
    EquipmentNameSearchForm,
    EquipmentAssignForm,
    RepairRequestSearchForm,
    RepairRequestForm,
)
from manager.models import Staff, Equipment, Category, RepairRequest


def index(request):
    """View function for the home page of the site."""

    num_staff = Staff.objects.count()
    num_equipment = Equipment.objects.count()
    num_categories = Category.objects.count()
    num_requests = RepairRequest.objects.count()
    new_requests = RepairRequest.objects.filter(status="pending").count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_staff": num_staff,
        "num_equipment": num_equipment,
        "num_categories": num_categories,
        "num_requests": num_requests,
        "num_visits": num_visits + 1,
        "new_requests": new_requests,
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
        queryset = super().get_queryset().prefetch_related("equipment")
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
    queryset = Category.objects.prefetch_related("equipment__assigned_to")


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
        queryset = Equipment.objects.select_related(
            "category"
        ).prefetch_related(
            "assigned_to"
        )
        form = EquipmentNameSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"].strip()
            )
        return queryset


class EquipmentDetailView(generic.DetailView):
    model = Equipment
    queryset = Equipment.objects.prefetch_related("assignments__employee")


class EquipmentCreateView(generic.CreateView):
    model = Equipment
    form_class = EquipmentForm


class EquipmentAssignmentView(generic.UpdateView):
    model = Equipment
    form_class = EquipmentAssignForm
    template_name = "manager/equipment_assign.html"

    def get_success_url(self):
        return reverse_lazy(
            "manager:equipment-detail",
            kwargs={"pk": self.object.pk}
        )


def delete_user_from_equipment(request, equipment_pk, user_id):
    equipment = get_object_or_404(Equipment, pk=equipment_pk)
    user = get_object_or_404(get_user_model(), pk=user_id)

    if user in equipment.assigned_to.all():
        equipment.assigned_to.remove(user)

    added_users = equipment.assigned_to.all()
    EquipmentAssignForm.base_fields[
        "assigned_to"
    ].queryset = get_user_model().objects.exclude(
        id__in=[u.id for u in added_users]
    )

    next_url = request.GET.get("next", "manager:index")
    return redirect(next_url, pk=equipment_pk)


class EquipmentUpdateView(generic.UpdateView):
    model = Equipment
    form_class = EquipmentForm


class EquipmentDeleteView(generic.DeleteView):
    model = Equipment
    success_url = reverse_lazy("manager:equipment-list")


class RepairRequestListView(generic.ListView):
    model = RepairRequest
    paginate_by = 10
    template_name = "manager/repair_request_list.html"
    context_object_name = "repair_request_list"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RepairRequestListView, self).get_context_data(**kwargs)
        equipment = self.request.GET.get("equipment", "")

        context["search_form"] = RepairRequestSearchForm(
            initial={"equipment": equipment}
        )
        return context


    def get_queryset(self):
        queryset = RepairRequest.objects.all()
        form = RepairRequestSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                equipment__name__icontains=form.cleaned_data["equipment"].strip()
            )
        return queryset


class RepairRequestDetailView(generic.DetailView):
    model = RepairRequest
    template_name = "manager/repair_request_detail.html"
    context_object_name = "repair_request"


class RepairRequestCreateView(generic.CreateView):
    model = RepairRequest
    template_name = "manager/repair_request_form.html"
    fields = ("equipment", "employee", "description")
    success_url = reverse_lazy("manager:repair-request-list")


class RepairRequestUserCreateView(generic.CreateView):
    model = RepairRequest
    template_name = "manager/repair_request_form.html"
    form_class = RepairRequestForm
    success_url = reverse_lazy("manager:repair-request-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["equipment"] = get_object_or_404(Equipment, pk=self.kwargs["equipment_pk"])
        kwargs["user"] = get_object_or_404(Staff, pk=self.kwargs["user_id"])
        return kwargs

    def form_valid(self, form):
        form.instance.equipment = get_object_or_404(Equipment, pk=self.kwargs["equipment_pk"])
        form.instance.employee = get_object_or_404(Staff, pk=self.kwargs["user_id"])
        return super().form_valid(form)


class RepairRequestUpdateView(generic.UpdateView):
    model = RepairRequest
    template_name = "manager/repair_request_form.html"
    fields = ("description", "status")


class RepairRequestDeleteView(generic.DeleteView):
    model = RepairRequest
    template_name = "manager/repair_request_confirm_delete.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next", reverse_lazy("manager:repair-request-list"))
        return next_url


def repair_request_update_status(request, pk):
    repair_request = get_object_or_404(RepairRequest, pk=pk)

    if repair_request.status == "in_progress":
        repair_request.status = "completed"
        repair_request.date_completed = datetime.now()
    elif repair_request.status == "pending":
        repair_request.status = "in_progress"

    repair_request.save()
    return redirect(reverse("manager:repair-request-list"))
