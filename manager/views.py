from django.shortcuts import render
from django.views import generic

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


class StaffDetailView(generic.DetailView):
    model = Staff


class CategoryListView(generic.ListView):
    model = Category


class EquipmentListView(generic.ListView):
    model = Equipment


class EquipmentDetailView(generic.DetailView):
    model = Equipment
