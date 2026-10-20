from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from django.contrib.auth import authenticate, login, logout


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    user = authenticate(
        username=request.data.get("username"),
        password=request.data.get("password"),
    )
    if user is None:
        return Response({"detail": "Invalid credentials"}, status=400)
    login(request, user)
    return Response({"username": user.username})


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response(status=204)


@api_view(["GET"])
@permission_classes([AllowAny])
def me_view(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Not authenticated"}, status=401)
    return Response({"username": request.user.username})