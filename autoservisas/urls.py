from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_nm'),
    path('cars/', views.cars, name='cars_nm'),
]
