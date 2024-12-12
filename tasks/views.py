from rest_framework import generics, status
from .models import Task, Category
from .serializers import (
    TaskSerializer,
    CategorySerializer,
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    TaskListSerializer,
    TaskCreateSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated, BasePermission, AllowAny
)
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


class IsTaskOwner(BasePermission):
    """
    Custom permission to only allow owners of a task to access or modify it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.owners.all()


class TaskListView(generics.ListAPIView):
    """
    List all tasks for the authenticated user with filtering options.
    Filters include priority and state.
    """
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(owners=self.request.user)
        priority = self.request.query_params.get('priority')
        state = self.request.query_params.get('state')

        if priority and priority not in ['low', 'medium', 'high']:
            queryset = queryset
        elif priority:
            queryset = queryset.filter(priority=priority)

        if state:
            queryset = queryset.filter(state=state)

        return queryset


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a category instance.
    Accessible only to authenticated users.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TaskCreateView(generics.CreateAPIView):
    """
    Create a new task and automatically assign the user as its owner.
    """
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owners=[self.request.user])

    def create(self, request, *args, **kwargs):
        print(f"Request Files: {request.FILES}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific task.
    Allows marking a task as completed via partial update.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]

    def get_serializer_context(self):
        """
        Add the request context to the serializer.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    def patch(self, request, *args, **kwargs):
        print("PATCH request data:", request.data)  # Debug incoming request
        task = self.get_object()
        print("Task before update:", task)  # Debug task instance

        serializer = self.get_serializer(task, data=request.data, partial=True)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)  # Debug validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        print("Task after update:", serializer.instance)  # Debug updated task
        return Response(serializer.data, status=status.HTTP_200_OK)



class CategoryListCreateView(generics.ListCreateAPIView):
    """
    List all categories or create a new category.
    Accessible only to authenticated users.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class RegisterView(APIView):
    """
    Handle user registration by creating a new user instance.
    """
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Authenticate users and provide access and refresh JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Logout a user by invalidating their refresh token.
    """
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"detail": "Logout successful"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthView(APIView):
    """
    Verify if the user is authenticated and return their details.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {
                    "isAuthenticated": True,
                    "user": {
                        "username": request.user.username,
                        "email": request.user.email,
                    },
                }
            )
        return Response(
            {
                "isAuthenticated": False,
                "message": (
                    "User not authenticated. You can still "
                    "register or log in."
                ),
            },
            status=status.HTTP_200_OK,
        )


def check_email(request):
    """
    Check if an email address exists in the system.
    Returns a JSON response indicating the result.
    """
    email = request.GET.get('email', None)
    if email:
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_exists': True})
        return JsonResponse({'email_exists': False})
    return JsonResponse({'error': 'Invalid request'}, status=400)
