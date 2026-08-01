from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .exports import ExportExcelView, ExportPdfView
from .token import FinanceTokenObtainView
from .views import (
    BudgetViewSet,
    ChargeViewSet,
    DashboardBudgetsView,
    DashboardComparatifView,
    DashboardEvolutionView,
    DashboardRepartitionView,
    FinanceUserDetailView,
    FinanceUsersView,
    TypeChargeViewSet,
)

router = DefaultRouter()
router.register(r'charges', ChargeViewSet, basename='finance-charge')
router.register(r'types', TypeChargeViewSet, basename='finance-type')
router.register(r'budgets', BudgetViewSet, basename='finance-budget')

urlpatterns = [
    # Auth
    path('auth/login/', FinanceTokenObtainView.as_view(), name='finance-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='finance-refresh'),

    # Dashboard
    path('dashboard/repartition/', DashboardRepartitionView.as_view(), name='finance-dashboard-repartition'),
    path('dashboard/evolution/', DashboardEvolutionView.as_view(), name='finance-dashboard-evolution'),
    path('dashboard/budgets/', DashboardBudgetsView.as_view(), name='finance-dashboard-budgets'),
    path('dashboard/comparatif/', DashboardComparatifView.as_view(), name='finance-dashboard-comparatif'),

    # Export
    path('export/pdf/', ExportPdfView.as_view(), name='finance-export-pdf'),
    path('export/excel/', ExportExcelView.as_view(), name='finance-export-excel'),

    # Gestion des utilisateurs finance (admin uniquement)
    path('admin/utilisateurs/', FinanceUsersView.as_view(), name='finance-admin-utilisateurs'),
    path('admin/utilisateurs/<int:pk>/', FinanceUserDetailView.as_view(), name='finance-admin-utilisateur-detail'),

    # CRUD charges / types / budgets
    path('', include(router.urls)),
]
