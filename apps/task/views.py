from rest_framework import generics
from .models import Day, Task
from .serializers import DaySerializer, TaskListSerializer, TaskDetailSerializer
from rest_framework.permissions import IsAuthenticated


class DayListAPIView(generics.ListAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        account = self.request.user
        day_id = self.kwargs.get('day_id')
        return qs.filter(account=account, day_id=day_id)


class TaskRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]