from rest_framework import serializers

from .models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "assignee",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def validate_project(self, project):
        if project.owner != self.context["request"].user:
            raise serializers.ValidationError("Project not found.")
        return project


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "owner", "tasks", "created_at"]
        read_only_fields = ["owner", "created_at"]
