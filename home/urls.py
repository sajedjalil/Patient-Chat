from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.inference, name='Patient Chat Home'),
    path('', views.index, name='Patient Chat Home'),
]

