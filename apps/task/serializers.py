from rest_framework import serializers
from .models import Day, Task


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ('day', )


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'is_completed')


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'