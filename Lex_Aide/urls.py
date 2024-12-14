from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lawapp.urls')),  # include app URLs
    path('', include('chatbot.urls')), 
    path('chatbot/', include('chatbot.urls')),
    
]