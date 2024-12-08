from rest_framework import generics, filters, status
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer, RegisterSerializer, LoginSerializer, LogoutSerializer, TaskListSerializer, TaskCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.response import Response
from django.utils import timezone

# Custom Permission
class IsTaskOwner(BasePermission):
    """
    Custom permission to only allow owners of a task to access or modify it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.owners.all()

class TaskListView(generics.ListAPIView):
    """
    View for listing tasks with filtering options.
    """
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(owners=self.request.user)
        priority = self.request.query_params.get('priority')
        state = self.request.query_params.get('state')
        if priority:
            queryset = queryset.filter(priority=priority)
        if state:
            queryset = queryset.filter(state=state)
        return queryset


# class TaskListView(generics.ListCreateAPIView):
#     """
#     GET: List all tasks with filtering capabilities.
#     """
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_fields = ['priority', 'state', 'category__name', 'owners__username', 'is_overdue']
#     search_fields = ['title', 'description']

class TaskCreateView(generics.CreateAPIView):
    """
    View for creating a new task.
    """
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the requesting user as an owner
        serializer.save(owners=[self.request.user])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

# RegisterView: Handles user registration.
class RegisterView(APIView):
    permission_classes = []  # No permissions required, so no auth needed.

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
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

# New check-auth endpoint to verify if the user is authenticated
class CheckAuthView(APIView):
    permission_classes = [AllowAny]  # Allow any user (even unauthenticated) to access this view

    def get(self, request):
        # Try to get the user from the request
        if request.user.is_authenticated:
            # If the user is authenticated, return the user data
            return Response({
                "isAuthenticated": True,
                "user": {
                    "username": request.user.username,
                    "email": request.user.email,
                }
            })
        
        # If the user is not authenticated, just return a message indicating it's not authenticated
        return Response({
            "isAuthenticated": False,
            "message": "User not authenticated. You can still register or log in."
        }, status=status.HTTP_200_OK)


# The check_email endpoint to verify if an email exists in the system
def check_email(request):
    email = request.GET.get('email', None)
    if email:
        # Check if email exists in the User model
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_exists': True})  # Return JSON if email exists
        else:
            return JsonResponse({'email_exists': False})  # Return JSON if email doesn't exist
    return JsonResponse({'error': 'Invalid request'}, status=400)  # Return error if email is missing
