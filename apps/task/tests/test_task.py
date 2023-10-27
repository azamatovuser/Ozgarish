from rest_framework.test import APITestCase
from apps.task.models import Day, Task
from apps.account.models import Account
from apps.task.serializers import TaskListSerializer, TaskDetailSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


class TaskListCreateTestCase(APITestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            username='test',
            password='123'
        )

        self.data_day_one = Day.objects.create(day=1)
        self.data_day_two = Day.objects.create(day=2)

        self.data_task_one = Task.objects.create(
            account=self.user,
            title='data',
            description='data',
            is_completed=False,
            day=self.data_day_one
        )
        self.data_task_two = Task.objects.create(
            account=self.user,
            title='more data',
            description='more data',
            is_completed=False,
            day=self.data_day_two
        )

    def test_get(self):
        user = get_user_model().objects.get(username='test')
        self.client.force_authenticate(user=user)

        response_day_one = self.client.get(f'/task/day/detail/{self.data_day_one.id}/task/')
        response_day_two = self.client.get(f'/task/day/detail/{self.data_day_two.id}/task/')

        serializer_data_day_one = TaskListSerializer(self.data_task_one).data
        serializer_data_day_two = TaskListSerializer(self.data_task_two).data


        self.assertEqual(response_day_one.data[0], serializer_data_day_one)
        self.assertEqual(response_day_two.data[0], serializer_data_day_two)


    def test_post(self):
        user = get_user_model().objects.get(username='test')
        self.client.force_authenticate(user=user)

        data_task = {
            'account': self.user.id,
            'title': 'data',
            'description': 'data',
            'is_completed': False,
            'day': self.data_day_one.id
        }

        response = self.client.post(f'/task/create/', data_task)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TaskRUDTestCase(APITestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            username='test',
            password='123'
        )
        self.client.force_authenticate(user=self.user)

        self.data_day_one = Day.objects.create(day=1)

        self.data_task_one = Task.objects.create(
            account=self.user,
            title='data',
            description='data',
            is_completed=False,
            day=self.data_day_one
        )


    def test_get(self):
        url = reverse('task_detail', kwargs={'day_id': self.data_day_one.id, 'pk': self.data_task_one.id})
        response = self.client.get(url)
        serializer_data = TaskDetailSerializer(self.data_task_one).data
        self.assertEqual(response.data, serializer_data)


    def test_patch(self):
        url = reverse('task_detail', kwargs={'day_id': self.data_day_one.id, 'pk': self.data_task_one.id})
        updated_data = {'title': 'Updated Title'}

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.data_task_one.refresh_from_db()
        self.assertEqual(self.data_task_one.title, updated_data['title'])

    def test_put(self):
        updated_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'is_completed': True,
            'day': self.data_day_one.id,
        }

        url = reverse('task_detail', kwargs={'day_id': self.data_day_one.id, 'pk': self.data_task_one.id})

        user = get_user_model().objects.get(username='test')
        self.client.force_authenticate(user=user)

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.data_task_one.refresh_from_db()

        self.assertEqual(self.data_task_one.title, updated_data['title'])
        self.assertEqual(self.data_task_one.description, updated_data['description'])
        self.assertEqual(self.data_task_one.is_completed, updated_data['is_completed'])
        self.assertEqual(self.data_task_one.day.id, updated_data['day'])