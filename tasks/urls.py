from django.urls import path  
from .views import (  
    TaskListCreateView, TaskRetrieveUpdateDestroyView,  
    CategoryListCreateView, RegisterView, LoginView, LogoutView
)  

urlpatterns = [  
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),  
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('register/', RegisterView.as_view(), name='register'),
    path('check-email/', check_email, name='check-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]  