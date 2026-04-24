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
