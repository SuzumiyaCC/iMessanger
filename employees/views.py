from django.views.generic import ListView
from .models import Employee


class EmployeeListView(ListView):
    template_name = "employees.html"
    context_object_name = "employees"
    queryset = Employee.objects.filter(is_active=True)
