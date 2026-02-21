from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "department", "email", "is_active")
    search_fields = ("full_name", "position", "department", "email")
    list_filter = ("department", "is_active")
