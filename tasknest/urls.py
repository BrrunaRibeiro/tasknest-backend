from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),  
    path('api/', include('tasks.urls')),  # This line includes the app's URLs
    path('api/auth/', include('dj_rest_auth.urls')),  
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')), 
    path('api/auth/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'), 
]
