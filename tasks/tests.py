from django.urls import reverse  
from rest_framework.test import APITestCase  
from rest_framework import status  
from .models import Task, Category  
from django.contrib.auth.models import User  

class TaskTests(APITestCase):  
    def setUp(self):  
        self.user = User.objects.create_user(username='testuser', password='pass')  
        self.client.login(username='testuser', password='pass')  
        self.category = Category.objects.create(name='Work')  

    def test_create_task_with_all_features(self):  
        url = reverse('task-list-create')  
        data = {  
            'title': 'Advanced Task',  
            'description': 'Testing advanced features.',  
            'due_date': '2025-12-31T23:59:59Z',  
            'priority': 'high',  
            'category_id': self.category.id,  
            'state': 'open',  
            'owner_ids': [self.user.id],  
        }  
        response = self.client.post(url, data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(Task.objects.count(), 1)  
        self.assertEqual(Task.objects.get().title, 'Advanced Task')  