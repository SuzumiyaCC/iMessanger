from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Employee


class EmployeeApiSearchPaginationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Employee.objects.create(
            full_name="Иван Иванов",
            position="Backend Engineer",
            email="ivanov@example.com",
            department="Engineering",
            is_active=True,
        )
        Employee.objects.create(
            full_name="Анна Петрова",
            position="HR Manager",
            email="petrova@example.com",
            department="HR",
            is_active=True,
        )
        Employee.objects.create(
            full_name="Сергей Смирнов",
            position="QA Engineer",
            email="smirnov@example.com",
            department="Engineering",
            is_active=False,
        )

    def test_search_by_q_matches_name_position_or_email(self):
        url = reverse("employee-list")

        by_name = self.client.get(url, {"q": "иван"})
        self.assertEqual(by_name.status_code, status.HTTP_200_OK)
        self.assertEqual(by_name.data["count"], 1)

        by_position = self.client.get(url, {"q": "hr manager"})
        self.assertEqual(by_position.status_code, status.HTTP_200_OK)
        self.assertEqual(by_position.data["count"], 1)

        by_email = self.client.get(url, {"q": "petrova@example.com"})
        self.assertEqual(by_email.status_code, status.HTTP_200_OK)
        self.assertEqual(by_email.data["count"], 1)

    def test_filter_by_department_and_only_active_employees(self):
        url = reverse("employee-list")
        response = self.client.get(url, {"department": "engineering"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # У неактивного QA тот же department, но в API он не должен попадать.
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["full_name"], "Иван Иванов")

    def test_mobile_pagination_contract(self):
        url = reverse("employee-list")
        response = self.client.get(url, {"page": 1, "page_size": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in ["count", "next", "previous", "page", "page_size", "results"]:
            self.assertIn(key, response.data)

        self.assertEqual(response.data["page"], 1)
        self.assertEqual(response.data["page_size"], 1)
        self.assertEqual(len(response.data["results"]), 1)
