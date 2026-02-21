from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.api_views import EmployeeViewSet
from news.api_views import PostViewSet
from corp_portal.views import HomeView
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
    path("api/", include(router.urls)),
]
