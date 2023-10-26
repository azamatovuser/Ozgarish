from rest_framework import generics
from .models import Day, Time, Task
from .serializers import DaySerializer, TaskListSerializer, \
    TaskDetailSerializer, TimeSerializer
from rest_framework.permissions import IsAuthenticated


class DayListAPIView(generics.ListAPIView):
    queryset = Day.objects.all()
    serializer_class = DaySerializer


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]


    # filtering tasks by day
    def get_queryset(self):
        qs = super().get_queryset()
        account = self.request.user
        day_id = self.kwargs.get('day_id')
        return qs.filter(account=account, day_id=day_id)


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]


class TaskRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated]


    # filtering task by account and day
    def get_queryset(self):
        qs = super().get_queryset()
        account = self.request.user
        day_id = self.kwargs.get('day_id')
        return qs.filter(account=account, day_id=day_id)


class TimeTotalAPIView(generics.ListAPIView):
    pass


class TimeCreateAPIView(generics.CreateAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer