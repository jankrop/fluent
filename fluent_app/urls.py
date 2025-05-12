from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('conversation/<int:pk>/', views.conversation, name='conversation'),
    path('conversation/<int:pk>/send', views.send_message, name='send_message'),
    path('message/<slug:task_id>/', views.check_message_status, name='check_message_status'),
]