import json
from datetime import datetime, timezone
from pathlib import Path

from django.conf import settings


class AuditTrailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith("/api/") and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            user = request.user.username if getattr(request, "user", None) and request.user.is_authenticated else "anonymous"
            payload = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "user": user,
            }
            log_dir = Path(settings.BASE_DIR) / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            with (log_dir / "audit.log").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

        return response
