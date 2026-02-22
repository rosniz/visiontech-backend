from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FormationViewSet

router = DefaultRouter()
router.register(r'', FormationViewSet, basename='formation')

urlpatterns = [
    path('', include(router.urls)),
]
