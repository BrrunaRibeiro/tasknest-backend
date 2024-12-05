from rest_framework import generics, filters
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer, RegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth import authenticate
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


# class RegisterView(APIView):
#     """Handles user registration."""
#     def post(self, request, *args, **kwargs):
#         print("Incoming request data:", request.data)  # Log request payload
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             print("Validation successful.")  # Log success
#             serializer.save()
#             return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
#         else:
#             print("Validation errors:", serializer.errors)  # Log errors
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # New LoginView for user authentication
# class LoginView(APIView):
#     """Handles user login."""
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         # Authenticate the user
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             # Generate JWT token
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
