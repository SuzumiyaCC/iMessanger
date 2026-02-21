from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db import connection


class HomeView(TemplateView):
    template_name = "home.html"


def health_api_view(request):
    db_ok = False
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_ok = cursor.fetchone()[0] == 1
    except Exception:
        db_ok = False

    return JsonResponse(
        {
            "service": "iMessanger",
            "status": "ok" if db_ok else "degraded",
            "db": "ok" if db_ok else "error",
        }
    )
