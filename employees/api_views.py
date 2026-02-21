from django.db.models import Q
from rest_framework import viewsets
from .models import Employee
from .pagination import EmployeeMobilePagination
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    # API-каталог ограничиваем активными сотрудниками для мобильного клиента.
    queryset = Employee.objects.filter(is_active=True).order_by("full_name", "id")
    serializer_class = EmployeeSerializer
    pagination_class = EmployeeMobilePagination

    def get_queryset(self):
        qs = super().get_queryset()
        q = (self.request.query_params.get("q") or "").strip()
        dept = (self.request.query_params.get("department") or "").strip()

        if q:
            qs = qs.filter(
                Q(full_name__icontains=q)
                | Q(position__icontains=q)
                | Q(email__icontains=q)
            )
        if dept:
            qs = qs.filter(department__icontains=dept)

        # distinct() защищает от дубликатов при расширении поиска/джойнах в будущем.
        return qs.distinct()
