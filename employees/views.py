from django.db.models import Q
from django.views.generic import ListView

from .models import Employee


class EmployeeListView(ListView):
    template_name = "employees.html"
    context_object_name = "employees"
    paginate_by = 12

    def get_queryset(self):
        qs = Employee.objects.filter(is_active=True).order_by("full_name", "id")
        q = (self.request.GET.get("q") or "").strip()
        department = (self.request.GET.get("department") or "").strip()

        if q:
            qs = qs.filter(
                Q(full_name__icontains=q)
                | Q(position__icontains=q)
                | Q(email__icontains=q)
            )
        if department:
            qs = qs.filter(department__icontains=department)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        ctx["department"] = (self.request.GET.get("department") or "").strip()
        return ctx
