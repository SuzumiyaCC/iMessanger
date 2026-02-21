from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class EmployeeMobilePagination(PageNumberPagination):
    """Pagination tuned for mobile clients (explicit page/page_size in payload)."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request) or self.page_size
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "page": self.page.number,
                "page_size": page_size,
                "results": data,
            }
        )
