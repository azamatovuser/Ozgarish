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

    def validate(self, data):
        request = self.context.get('request')
        day_id = request.GET.get('day_id')
        account = request.user
        task = self.instance

        if task.account != account:
            raise serializers.ValidationError("You are not allowed to access this task.")

        if task.day_id != day_id:
            raise serializers.ValidationError("Not Found 404")

        return data