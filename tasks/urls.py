from django.urls import path  
from .views import (  
    TaskRetrieveUpdateDestroyView,  
    CategoryListCreateView, RegisterView, LoginView, LogoutView, check_email,
    CheckAuthView, TaskCreateView, TaskListView, CategoryRetrieveUpdateDestroyView
)  

urlpatterns = [  
    path('tasks/', TaskListView.as_view(), name='task-list'),  
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('create-task/', TaskCreateView.as_view(), name='task-create'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('check-email/', check_email, name='check-email'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]  