from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, TaskViewSet, login_view, logout_view, me_view

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = router.urls + [
    path("auth/login/", login_view),
    path("auth/logout/", logout_view),
    path("auth/me/", me_view),
]
