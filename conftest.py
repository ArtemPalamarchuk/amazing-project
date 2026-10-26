import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from api.models import Project, Task

PASSWORD = "test-password"


@pytest.fixture
def password():
    return PASSWORD


@pytest.fixture
def alice():
    return get_user_model().objects.create_user("alice", password=PASSWORD)


@pytest.fixture
def bob():
    return get_user_model().objects.create_user("bob", password=PASSWORD)


@pytest.fixture
def alice_project(alice):
    return Project.objects.create(name="Alice project", owner=alice)


@pytest.fixture
def bob_project(bob):
    return Project.objects.create(name="Bob project", owner=bob)


@pytest.fixture
def alice_task(alice_project):
    return Task.objects.create(project=alice_project, title="Alice task")


@pytest.fixture
def bob_task(bob_project):
    return Task.objects.create(project=bob_project, title="Bob task")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def alice_client(alice):
    client = APIClient()
    client.force_authenticate(user=alice)
    return client
