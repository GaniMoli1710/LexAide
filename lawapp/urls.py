#from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('home', views.home, name='home'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('legal-research/', views.legal_research, name='legal_research'),
    path('document-analysis/', views.document_analysis, name='document_analysis'),
    path('legal-support/', views.legal_support, name='legal_support'),
    path('legal-bot/', views.legal_bot, name='legal_bot'),
    path('profile',views.profile, name='profile'),
    path('upload/', views.upload_document, name='upload_document'),
    path('download-report/', views.download_report, name='download_report'),
    path('chatbot/', include('chatbot.urls')),

]