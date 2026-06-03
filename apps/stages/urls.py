from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, MesDemandesView, DemandeDetailView,
    AdminDemandesListView, AdminDemandeDetailView,
    AdminDecisionView, AdminStatsView,
)
from .token import EmailTokenObtainView

urlpatterns = [
    # Auth candidat
    path('auth/register/', RegisterView.as_view(),        name='stage-register'),
    path('auth/login/',    EmailTokenObtainView.as_view(), name='stage-login'),
    path('auth/refresh/',  TokenRefreshView.as_view(),     name='stage-refresh'),

    # Candidat
    path('',        MesDemandesView.as_view(),  name='stage-mes-demandes'),
    path('<int:pk>/', DemandeDetailView.as_view(), name='stage-detail'),

    # Admin
    path('admin/liste/',            AdminDemandesListView.as_view(),  name='admin-stages-liste'),
    path('admin/stats/',            AdminStatsView.as_view(),         name='admin-stages-stats'),
    path('admin/<int:pk>/',         AdminDemandeDetailView.as_view(), name='admin-stage-detail'),
    path('admin/<int:pk>/decision/', AdminDecisionView.as_view(),     name='admin-stage-decision'),
]
