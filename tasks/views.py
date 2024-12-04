from rest_framework import generics, filters
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer, RegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(APIView):
    """Handles user registration."""
    def post(self, request, *args, **kwargs):
        print("Incoming request data:", request.data)  # Log request payload
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            print("Validation successful.")  # Log success
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)  # Log errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # print("Request received at RegisterView")  # Log when the request reaches the view
        # print("Request data:", request.data, request.body)  # Log the incoming request data

        # # Use the updated RegisterSerializer
        # serializer = RegisterSerializer(data=request.data)
        
        # # Check if the serializer is valid
        # if serializer.is_valid():
        #     print("Serializer is valid")  # Log if the serializer validation passes
        #     serializer.save()  # Save the user data
        #     return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        # # Log and return errors if serializer is invalid
        # print("Serializer errors:", serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
