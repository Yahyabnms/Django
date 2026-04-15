from django.urls import path
from . import views

app_name = 'assurance'

urlpatterns = [
    path('', views.assurance_list, name='list'),
    path('<int:pk>/', views.assurance_detail, name='detail'),
]
