from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Patient Chat Home'),
    path("chat/", views.inference, name='Patient Chat Home'),
    path('insight/', views.insight, name='insight'),
    path('user-info/', views.get_user_info, name='user_info'),
    path('thread-id/', views.get_unique_thread_id, name='thread-id')
]
