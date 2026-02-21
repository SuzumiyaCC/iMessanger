from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = (self.request.query_params.get("q") or "").strip()
        dept = (self.request.query_params.get("department") or "").strip()

        if q:
            qs = qs.filter(full_name__icontains=q)
        if dept:
            qs = qs.filter(department__icontains=dept)
        return qs
