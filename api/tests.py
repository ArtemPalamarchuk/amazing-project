import pytest

from .models import Task

# Auth


@pytest.mark.django_db
def test_login_ok(api_client, alice, password):
    response = api_client.post(
        "/api/auth/login/",
        {"username": "alice", "password": password},
        format="json",
    )
    assert response.status_code == 200
    assert response.data["username"] == "alice"


@pytest.mark.django_db
def test_login_invalid(api_client, alice):
    response = api_client.post(
        "/api/auth/login/",
        {"username": "alice", "password": "wrong"},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_me_anonymous(api_client):
    response = api_client.get("/api/auth/me/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_projects_require_auth(api_client):
    response = api_client.get("/api/projects/")
    assert response.status_code == 403


# Project permissions


@pytest.mark.django_db
def test_list_only_own_projects(alice_client, alice_project, bob_project):
    response = alice_client.get("/api/projects/")
    assert response.status_code == 200
    assert [p["id"] for p in response.data["results"]] == [alice_project.id]


@pytest.mark.django_db
def test_cannot_open_foreign_project(alice_client, bob_project):
    response = alice_client.get(f"/api/projects/{bob_project.id}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_sets_owner(alice_client, alice, bob):
    response = alice_client.post(
        "/api/projects/",
        {"name": "New project", "owner": bob.id},
        format="json",
    )
    assert response.status_code == 201
    project = alice.projects.get(id=response.data["id"])
    assert project.owner == alice


# Task permissions


@pytest.mark.django_db
def test_list_hides_foreign_tasks(alice_client, alice_task, bob_task):
    response = alice_client.get("/api/tasks/")
    assert response.status_code == 200
    assert [t["id"] for t in response.data["results"]] == [alice_task.id]


@pytest.mark.django_db
def test_create_task_in_own_project(alice_client, alice_project):
    response = alice_client.post(
        "/api/tasks/",
        {"project": alice_project.id, "title": "Mine"},
        format="json",
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_cannot_create_task_in_foreign_project(alice_client, bob_project):
    response = alice_client.post(
        "/api/tasks/",
        {"project": bob_project.id, "title": "hack"},
        format="json",
    )
    assert response.status_code == 400
    assert not Task.objects.filter(title="hack").exists()


@pytest.mark.django_db
def test_cannot_move_task_to_foreign_project(
    alice_client, alice_task, alice_project, bob_project
):
    response = alice_client.patch(
        f"/api/tasks/{alice_task.id}/",
        {"project": bob_project.id},
        format="json",
    )
    assert response.status_code == 400
    alice_task.refresh_from_db()
    assert alice_task.project_id == alice_project.id
