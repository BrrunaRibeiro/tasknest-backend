from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),  # Includes task-related endpoints
    path('api/auth/', include('dj_rest_auth.urls')),  # Auth-related endpoints
    path(
        'api/auth/registration/',
        include('dj_rest_auth.registration.urls'),  # Registration endpoints
    ),
    path(
        'api/auth/token/blacklist/',
        TokenBlacklistView.as_view(),
        name='token_blacklist',  # Endpoint for blacklisting tokens
    ),
]
