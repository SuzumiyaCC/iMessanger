from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.api_views import EmployeeViewSet
from employees.auth_api import LoginApiView, ProfileApiView
from news.api_views import PostViewSet
from corp_portal.views import HomeView
from corp_portal.views import health_api_view
from employees.views import EmployeeListView
from news.views import PostListView

router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("employees/", EmployeeListView.as_view(), name="employees"),
    path("news/", PostListView.as_view(), name="news"),
    path("api/auth/login/", LoginApiView.as_view(), name="api-login"),
    path("api/auth/me/", ProfileApiView.as_view(), name="api-me"),
    path("api/health/", health_api_view, name="api-health"),
    path("api/", include(router.urls)),
]
