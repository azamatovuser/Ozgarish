from rest_framework import serializers
from .models import Day, Time, Task


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ('day', )


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = ('hours', 'minutes')


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'is_completed')


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'