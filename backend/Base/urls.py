from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, SignUpView, LoginView, ProfileView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]