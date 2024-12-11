from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task, Category
from django.contrib.auth.models import User
from datetime import datetime, timezone
from rest_framework_simplejwt.tokens import RefreshToken


class TaskTests(APITestCase):
    def setUp(self):
        """
        Set up a user, category, and login for tests.
        """
        # Create user
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.category = Category.objects.create(name='Work')

        # Generate JWT token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Authenticate requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_task_with_all_features(self):
        """
        Test creating a task with all features provided.
        """
        url = reverse('task-create')
        data = {
            'title': 'Advanced Task',
            'description': 'Testing advanced features.',
            'due_date': datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat(),
            'priority': 'high',
            'category_id': self.category.id,
            'state': 'open',
            'owner_ids': [self.user.id],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Advanced Task')

    def test_create_task_missing_title(self):
        """
        Test creating a task without a title.
        """
        url = reverse('task-create')
        data = {
            'description': 'Missing title.',
            'due_date': datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat(),
            'priority': 'medium',
            'category_id': self.category.id,
            'state': 'open',
            'owner_ids': [self.user.id],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_create_task_invalid_due_date(self):
        """
        Test creating a task with an invalid due date in the past.
        """
        url = reverse('task-create')
        data = {
            'title': 'Invalid Due Date',
            'description': 'Testing invalid due date.',
            'due_date': datetime(2020, 12, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat(),
            'priority': 'high',
            'category_id': self.category.id,
            'state': 'open',
            'owner_ids': [self.user.id],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('due_date', response.data)

    def test_retrieve_task_authenticated_user(self):
        """
        Test retrieving a task by an authenticated user.
        """
        task = Task.objects.create(
            title='Test Task',
            description='A task to retrieve.',
            due_date=datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
            priority='low',
            state='open',
            category=self.category,
        )
        task.owners.add(self.user)
        url = reverse('task-detail', args=[task.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], task.title)

    def test_unauthorized_access(self):
        """
        Test accessing tasks without authorization.
        """
        self.client.credentials()  # Clear authentication
        url = reverse('task-create')
        data = {
            'title': 'Unauthorized Access',
            'description': 'Testing unauthorized access.',
            'due_date': datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc).isoformat(),
            'priority': 'low',
            'category_id': self.category.id,
            'state': 'open',
            'owner_ids': [self.user.id],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
