from django.urls import path
from .views import (
    TaskRetrieveUpdateDestroyView,
    CategoryListCreateView,
    RegisterView,
    LoginView,
    LogoutView,
    check_email,
    CheckAuthView,
    TaskCreateView,
    TaskListView,
    CategoryRetrieveUpdateDestroyView,
)

# URL patterns for the API endpoints
urlpatterns = [
    path(
        'tasks/',
        TaskListView.as_view(),
        name='task-list',
    ),  # List all tasks for the authenticated user
    path(
        'tasks/<int:pk>/',
        TaskRetrieveUpdateDestroyView.as_view(),
        name='task-detail',
    ),  # Retrieve, update, or delete a specific task
    path(
        'create-task/',
        TaskCreateView.as_view(),
        name='task-create',
    ),  # Create a new task
    path(
        'categories/',
        CategoryListCreateView.as_view(),
        name='category-list-create',
    ),  # List all categories or create a new one
    path(
        'categories/<int:pk>/',
        CategoryRetrieveUpdateDestroyView.as_view(),
        name='category-detail',
    ),  # Retrieve, update, or delete a category
    path(
        'register/',
        RegisterView.as_view(),
        name='register',
    ),  # Register a new user
    path(
        'check-email/',
        check_email,
        name='check-email',
    ),  # Check if an email exists
    path(
        'check-auth/',
        CheckAuthView.as_view(),
        name='check-auth',
    ),  # Check if the user is authenticated
    path(
        'login/',
        LoginView.as_view(),
        name='login',
    ),  # Log in a user and provide tokens
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout',
    ),  # Log out a user
]
