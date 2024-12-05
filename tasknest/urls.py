from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),  # Make sure the tasks app is set up correctly
    path('api/auth/', include('dj_rest_auth.urls')),  # Handles login, logout, etc.
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Handles registration
    path('api/auth/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),  # Handles token blacklisting
]
