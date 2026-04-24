from datetime import timedelta

import pytest
from django.utils import timezone

from tasks.models import Task


@pytest.mark.django_db
def test_task_defaults_done_to_false():
    task = Task.objects.create(title="Buy milk")

    assert task.title == "Buy milk"
    assert task.done is False
    assert task.created_at is not None


@pytest.mark.django_db
def test_task_str_returns_title():
    task = Task.objects.create(title="Walk the dog")

    assert str(task) == "Walk the dog"


@pytest.mark.django_db
def test_tasks_ordered_by_created_at_desc():
    now = timezone.now()
    # created_at is auto_now_add, so we assign explicit times via update()
    # to avoid sub-millisecond ties between Task.objects.create() calls.
    first = Task.objects.create(title="First")
    Task.objects.filter(pk=first.pk).update(created_at=now - timedelta(minutes=2))
    second = Task.objects.create(title="Second")
    Task.objects.filter(pk=second.pk).update(created_at=now - timedelta(minutes=1))
    third = Task.objects.create(title="Third")
    Task.objects.filter(pk=third.pk).update(created_at=now)

    titles = list(Task.objects.values_list("title", flat=True))

    assert titles == ["Third", "Second", "First"]
