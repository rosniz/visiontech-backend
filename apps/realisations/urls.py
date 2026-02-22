from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RealisationViewSet

router = DefaultRouter()
router.register(r'', RealisationViewSet, basename='realisation')

urlpatterns = [
    path('', include(router.urls)),
]
