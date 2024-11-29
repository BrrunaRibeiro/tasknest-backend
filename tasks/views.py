from rest_framework import generics, filters  
from .models import Task, Category  
from .serializers import TaskSerializer, CategorySerializer  
from django_filters.rest_framework import DjangoFilterBackend  
from rest_framework.permissions import IsAuthenticated  

class TaskListCreateView(generics.ListCreateAPIView):  
    """  
    GET: List all tasks with filtering capabilities.  
    POST: Create a new task.  
    """  
    queryset = Task.objects.all()  
    serializer_class = TaskSerializer  
    permission_classes = [IsAuthenticated]  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  
    filterset_fields = ['priority', 'state', 'category__name', 'owners__username', 'is_overdue']  
    search_fields = ['title', 'description']  

    def perform_create(self, serializer):  
        """  
        Set the current user as an owner if not specified.  
        """  
        serializer.save()  

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):  
    """  
    GET: Retrieve a task by ID.  
    PUT/PATCH: Update a task.  
    DELETE: Delete a task.  
    """  
    queryset = Task.objects.all()  
    serializer_class = TaskSerializer  
    permission_classes = [IsAuthenticated] 

class CategoryListCreateView(generics.ListCreateAPIView):  
    """  
    GET: List all categories.  
    POST: Create a new category.  
    """  
    queryset = Category.objects.all()  
    serializer_class = CategorySerializer  
    permission_classes = [IsAuthenticated]  