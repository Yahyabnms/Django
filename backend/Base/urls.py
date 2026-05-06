from django.urls import path
from .views import HomeView, SignUpView, LoginView, ProfileView, MesReservationsView, MesContratsView, CustomLogoutView
from Voiture.views import ListeVoituresView, VerifierDisponibiliteView, SuiviGPSView, APIGPSVoiture, DashboardGPSView, APIAllCarsGPS

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('mes-reservations/', MesReservationsView.as_view(), name='mes-reservations'),
    path('mes-contrats/', MesContratsView.as_view(), name='mes-contrats'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('voitures/', ListeVoituresView.as_view(), name='liste-voitures'),
    path('voiture/<int:voiture_id>/verifier-disponibilite/', VerifierDisponibiliteView.as_view(), name='verifier-disponibilite'),
    path('voiture/<int:voiture_id>/suivi-gps/', SuiviGPSView.as_view(), name='suivi-gps'),
    path('dashboard-gps/', DashboardGPSView.as_view(), name='dashboard-gps'),
    path('api/voiture/<int:voiture_id>/gps/', APIGPSVoiture.as_view(), name='api-gps-voiture'),
    path('api/voitures/gps/', APIAllCarsGPS.as_view(), name='api-all-cars-gps'),
]