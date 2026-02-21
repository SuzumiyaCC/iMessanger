from django.db.models import Q
from django.db.models.functions import Lower
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

        # Для PostgreSQL/кириллицы используем LOWER(field) + contains(lower(query)),
        # чтобы поведение было воспроизводимым независимо от collation окружения.
        if q:
            q_norm = q.casefold()
            qs = qs.annotate(
                full_name_ci=Lower("full_name"),
                position_ci=Lower("position"),
                email_ci=Lower("email"),
            ).filter(
                Q(full_name_ci__contains=q_norm)
                | Q(position_ci__contains=q_norm)
                | Q(email_ci__contains=q_norm)
            )

        if dept:
            dept_norm = dept.casefold()
            qs = qs.annotate(department_ci=Lower("department")).filter(
                department_ci__contains=dept_norm
            )

        # distinct() защищает от дубликатов при расширении поиска/джойнах в будущем.
        return qs.distinct()

    @action(detail=True, methods=["get"], url_path="quick-contact")
    def quick_contact(self, request, pk=None):
        employee = self.get_object()

        # Fallback: если отдельного мессенджера нет в данных,
        # используем локальную часть email как Telegram handle для быстрой связи.
        email_local = (employee.email or "").split("@")[0]
        messenger_handle = f"@{email_local}" if email_local else ""
        messenger_link = f"https://t.me/{email_local}" if email_local else ""

        cta_link = ""
        cta_type = ""
        if employee.phone:
            cta_type, cta_link = "phone", f"tel:{employee.phone}"
        elif employee.email:
            cta_type, cta_link = "email", f"mailto:{employee.email}"
        elif messenger_link:
            cta_type, cta_link = "messenger", messenger_link

        return Response(
            {
                "id": employee.id,
                "full_name": employee.full_name,
                "quick_contact": {
                    "phone": employee.phone,
                    "email": employee.email,
                    "messenger": messenger_handle,
                    "messenger_link": messenger_link,
                },
                "cta": {
                    "type": cta_type,
                    "link": cta_link,
                    "preferred_channel": cta_type,
                },
            }
        )
