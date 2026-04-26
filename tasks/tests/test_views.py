import uuid
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task


@pytest.mark.django_db
def test_list_empty_returns_empty_array(client):
    response = client.get(reverse("task-list"))

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_list_returns_all_tasks(client):
    Task.objects.create(title="Buy milk")
    Task.objects.create(title="Walk the dog")

    response = client.get(reverse("task-list"))

    assert response.status_code == 200
    titles = {t["title"] for t in response.json()}
    assert titles == {"Buy milk", "Walk the dog"}


@pytest.mark.django_db
def test_list_orders_newer_tasks_first(client):
    now = timezone.now()
    oldest = Task.objects.create(title="Oldest")
    Task.objects.filter(pk=oldest.pk).update(created_at=now - timedelta(minutes=10))
    middle = Task.objects.create(title="Middle")
    Task.objects.filter(pk=middle.pk).update(created_at=now - timedelta(minutes=5))
    newest = Task.objects.create(title="Newest")
    Task.objects.filter(pk=newest.pk).update(created_at=now)

    response = client.get(reverse("task-list"))

    titles = [t["title"] for t in response.json()]
    assert titles == ["Newest", "Middle", "Oldest"]


@pytest.mark.django_db
def test_list_exposes_expected_fields(client):
    Task.objects.create(title="Buy milk")

    response = client.get(reverse("task-list"))

    [task] = response.json()
    assert set(task.keys()) == {"id", "title", "done", "created_at"}
    assert task["title"] == "Buy milk"
    assert task["done"] is False
    # id must be a UUID (not an enumerable int) — raises ValueError otherwise.
    uuid.UUID(task["id"])


@pytest.mark.django_db
def test_create_task_returns_201_and_persists(client):
    response = client.post(
        reverse("task-list"),
        data={"title": "Buy bread"},
        content_type="application/json",
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Buy bread"
    assert body["done"] is False
    uuid.UUID(body["id"])
    assert Task.objects.filter(title="Buy bread").exists()


@pytest.mark.django_db
def test_create_without_title_returns_400(client):
    response = client.post(
        reverse("task-list"),
        data={},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "title" in response.json()
    assert Task.objects.count() == 0


@pytest.mark.django_db
def test_create_with_blank_title_returns_400(client):
    response = client.post(
        reverse("task-list"),
        data={"title": ""},
        content_type="application/json",
    )

    assert response.status_code == 400
    assert Task.objects.count() == 0
