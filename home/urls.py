from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Patient Chat Home')
]
