from django.urls import path  
from .views import (  
    TaskListCreateView, TaskRetrieveUpdateDestroyView,  
    CategoryListCreateView, RegisterView, LoginView, LogoutView, check_email,
    CheckAuthView, TaskCreateView, TaskListView
)  

urlpatterns = [  
    path('tasks/', TaskListView.as_view(), name='task-list'),  
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('tasks-create/', TaskCreateView.as_view(), name='task-create')
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('register/', RegisterView.as_view(), name='register'),
    path('check-email/', check_email, name='check-email'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]  