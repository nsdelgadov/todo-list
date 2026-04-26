from rest_framework import mixins, permissions, viewsets

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
