from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticlePublicViewSet, CategorieListView, TagListView, ArticlesPopulairesView,
    ArticleAdminViewSet, CategorieAdminViewSet, TagAdminViewSet, BlogDashboardStatsView,
)

# Public
public_router = DefaultRouter()
public_router.register('articles', ArticlePublicViewSet, basename='blog-article')

# Admin
admin_router = DefaultRouter()
admin_router.register('articles', ArticleAdminViewSet, basename='blog-admin-article')
admin_router.register('categories', CategorieAdminViewSet, basename='blog-admin-categorie')
admin_router.register('tags', TagAdminViewSet, basename='blog-admin-tag')

urlpatterns = [
    path('categories/', CategorieListView.as_view(), name='blog-categories'),
    path('tags/', TagListView.as_view(), name='blog-tags'),
    path('populaires/', ArticlesPopulairesView.as_view(), name='blog-populaires'),
    path('admin/stats/', BlogDashboardStatsView.as_view(), name='blog-admin-stats'),
    path('admin/', include(admin_router.urls)),
    path('', include(public_router.urls)),
]
