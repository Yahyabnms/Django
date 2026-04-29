from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListReservationView.as_view(), name='reservation-list'),
    path('<int:pk>/', views.DetailReservationView.as_view(), name='reservation-detail'),
    path('create/', views.CreateReservationView.as_view(), name='reservation-create'),
    path('reserver/<int:voiture_id>/', views.ReserverVoitureView.as_view(), name='reserver-voiture'),
    path('api/check-availability/<int:voiture_id>/', views.check_availability, name='check-availability'),
    path('api/create-reservation/', views.create_reservation, name='create-reservation'),
]
