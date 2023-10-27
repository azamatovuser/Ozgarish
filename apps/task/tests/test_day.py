from rest_framework.test import APITestCase
from apps.task.models import Day
from apps.task.serializers import DaySerializer
from rest_framework import status


class DayListTestCase(APITestCase):
    def setUp(self):
        self.data_one = Day.objects.create(day=1)
        self.data_two = Day.objects.create(day=2)

    def test_get(self):
        response = self.client.get('/task/day/list/')
        serializer_data = DaySerializer([self.data_one, self.data_two], many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)