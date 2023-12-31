from rest_framework import generics
from .models import Day, Time, Task
from .serializers import DaySerializer, TaskListSerializer, \
    TaskDetailSerializer, TimeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
    serializer_class = TimeSerializer

    def get_queryset(self):
        day_id = self.kwargs['day_id']
        queryset = Time.objects.filter(task__day_id=day_id)
        return queryset

    def get_total_time(self, queryset):
        total_hours = sum([time.hours for time in queryset])
        total_minutes = sum([time.minutes for time in queryset])
        total_hours += total_minutes // 60
        total_minutes %= 60
        return {"hours": total_hours, "minutes": total_minutes}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_time = self.get_total_time(queryset)
        return Response(total_time)


class TimeCreateAPIView(generics.CreateAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer