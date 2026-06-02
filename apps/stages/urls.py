from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, MesDemandesView, DemandeDetailView
from .token import EmailTokenObtainView

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(),        name='stage-register'),
    path('auth/login/',    EmailTokenObtainView.as_view(), name='stage-login'),
    path('auth/refresh/',  TokenRefreshView.as_view(),     name='stage-refresh'),

    # Demandes
    path('',       MesDemandesView.as_view(),  name='stage-mes-demandes'),
    path('<int:pk>/', DemandeDetailView.as_view(), name='stage-detail'),
]
