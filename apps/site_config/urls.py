from django.urls import path
from .views import StatutSiteView, ParametresSiteAdminView

urlpatterns = [
    path('status/',          StatutSiteView.as_view(),          name='site-status'),
    path('admin/settings/',  ParametresSiteAdminView.as_view(), name='site-admin-settings'),
]
