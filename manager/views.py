from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from manager.forms import StaffForm, StaffUpdateForm, EquipmentForm
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


class StaffDetailView(generic.DetailView):
    model = Staff


class StaffCreateView(generic.CreateView):
    model = Staff
    form_class = StaffForm


class StaffUpdateView(generic.UpdateView):
    model = Staff
    form_class = StaffUpdateForm


class StaffDeleteView(generic.DeleteView):
    model = Staff
    success_url = reverse_lazy("manager:staff-list")


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10


class CategoryCreateView(generic.CreateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("manager:category-list")


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


class EquipmentDetailView(generic.DetailView):
    model = Equipment


class EquipmentCreateView(generic.CreateView):
    model = Equipment
    form_class = EquipmentForm


class EquipmentUpdateView(generic.UpdateView):
    model = Equipment
    form_class = EquipmentForm


class EquipmentDeleteView(generic.DeleteView):
    model = Equipment
    success_url = reverse_lazy("manager:equipment-list")
