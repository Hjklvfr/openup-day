from django.urls import path

from app import views

urlpatterns = [
    path('', views.login, name='login'),
    path('chat/<str:room_name>/', views.chat, name='chat')
]
