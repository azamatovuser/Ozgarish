from rest_framework.test import APITestCase
from apps.task.models import Time, Task, Day
from apps.account.models import Account
from django.urls import reverse
from rest_framework import status


class TimeTestCase(APITestCase):
    def setUp(self):
        self.day_data = Day.objects.create(day=1)

        self.user = Account.objects.create_user(
            username='test',
            password='123'
        )

        self.task = Task.objects.create(
            account=self.user,
            title='title',
            description='description',
            is_completed=False,
            day=self.day_data
        )

    def test_post(self):
        time_data = {
            'hours': 2,
            'minutes': 30,
            'task': self.task.id
        }
        response = self.client.post('/task/time/create/', time_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['hours'], 2)
        self.assertEqual(response.data['minutes'], 30)

    def test_get(self):
        Time.objects.create(hours=2, minutes=30, task=self.task)
        Time.objects.create(hours=1, minutes=45, task=self.task)
        Time.objects.create(hours=3, minutes=15, task=self.task)

        response = self.client.get(reverse('day-total-time', args=[self.day_data.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        total_hours = sum([time.hours for time in Time.objects.filter(task=self.task)])
        total_minutes = sum([time.minutes for time in Time.objects.filter(task=self.task)])
        total_hours += total_minutes // 60
        total_minutes %= 60
        expected_total_time = {"hours": total_hours, "minutes": total_minutes}

        self.assertEqual(response.data['hours'], expected_total_time['hours'])
        self.assertEqual(response.data['minutes'], expected_total_time['minutes'])
