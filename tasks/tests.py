from django.urls import reverse  
from rest_framework.test import APITestCase  
from rest_framework import status  
from .models import Task  

class TaskTests(APITestCase):  
    """  
    Contains tests for Task API endpoints.  
    """  

    def test_create_task(self):  
        """  
        Ensure we can create a new task.  
        """  
        url = reverse('task-list-create')  
        data = {'title': 'Test Task', 'description': 'Description'}  
        self.client.force_authenticate(user=None)  # Authenticate if necessary  
        response = self.client.post(url, data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(Task.objects.count(), 1)  
        self.assertEqual(Task.objects.get().title, 'Test Task')  