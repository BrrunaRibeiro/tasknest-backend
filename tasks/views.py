from rest_framework import generics, filters
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer, RegisterSerializer, LoginSerializer, LogoutSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# Custom Permission
class IsTaskOwner(BasePermission):
    """
    Custom permission to only allow owners of a task to access or modify it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.owners.all()


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
        serializer.save(owners=[self.request.user])  # Automatically assign the requesting user as an owner.


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a task by ID.
    PUT/PATCH: Update a task.
    DELETE: Delete a task.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]  # Added IsTaskOwner permission


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    GET: List all categories.
    POST: Create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# In views.py, for RegisterView
class RegisterView(APIView):
    """Handles user registration."""
    permission_classes = []  # No permissions required, so no auth needed.

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

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Use the LoginSerializer to validate and authenticate the user
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']  # Access the user object
            refresh = RefreshToken.for_user(user)  # Generate the refresh token
            return Response({
                'access': str(refresh.access_token),  # Send back access token
                'refresh': str(refresh)  # Send back refresh token
            })

        # If validation fails, return the error details
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)