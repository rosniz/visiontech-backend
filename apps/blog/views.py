from django.utils import timezone
from django.db.models import Sum
from rest_framework import viewsets, filters, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Article, Categorie, Tag
from .serializers import (
    ArticleListSerializer, ArticleDetailSerializer, ArticleWriteSerializer,
    CategorieSerializer, TagSerializer,
)
from .pagination import BlogPagination


# ── Public ────────────────────────────────────────────────────────────────────

class ArticlePublicViewSet(viewsets.ReadOnlyModelViewSet):
    """Endpoints publics du blog : liste + détail (uniquement les articles publiés)."""
    permission_classes = [AllowAny]
    pagination_class   = BlogPagination
    lookup_field        = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'categorie__slug': ['exact'],
        'tags__slug':      ['exact'],
    }
    search_fields  = ['titre', 'sous_titre', 'extrait', 'contenu', 'tags__nom', 'categorie__nom']
    ordering_fields = ['date_publication', 'vues', 'temps_lecture']
    ordering        = ['-date_publication']

    def get_queryset(self):
        return Article.objects.publies().select_related('categorie').prefetch_related('tags', 'galerie').distinct()

    def get_serializer_class(self):
        return ArticleDetailSerializer if self.action == 'retrieve' else ArticleListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.incrementer_vues()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategorieListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class   = CategorieSerializer
    queryset           = Categorie.objects.all()
    pagination_class   = None


class TagListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class   = TagSerializer
    queryset           = Tag.objects.all()
    pagination_class   = None


class ArticlesPopulairesView(generics.ListAPIView):
    """Top articles par vues — utilisé pour les widgets 'populaire'."""
    permission_classes = [AllowAny]
    serializer_class   = ArticleListSerializer
    pagination_class   = None

    def get_queryset(self):
        return Article.objects.publies().order_by('-vues')[:5]


# ── Admin (CMS) ────────────────────────────────────────────────────────────────

class ArticleAdminViewSet(viewsets.ModelViewSet):
    """CRUD complet réservé aux admins, incluant brouillons et programmés."""
    permission_classes = [IsAdminUser]
    pagination_class   = BlogPagination
    lookup_field        = 'pk'
    queryset            = Article.objects.all().select_related('categorie').prefetch_related('tags')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'categorie', 'mis_en_avant']
    search_fields    = ['titre', 'extrait', 'contenu']
    ordering_fields  = ['date_publication', 'created_at', 'vues', 'titre']
    ordering         = ['-created_at']

    def get_serializer_class(self):
        return ArticleWriteSerializer if self.action in ('create', 'update', 'partial_update') else ArticleDetailSerializer


class CategorieAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class   = CategorieSerializer
    queryset           = Categorie.objects.all()
    pagination_class   = None


class TagAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class   = TagSerializer
    queryset           = Tag.objects.all()
    pagination_class   = None


class BlogDashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Article.objects.all()
        total_vues = qs.aggregate(total=Sum('vues'))['total'] or 0
        top = qs.publies().order_by('-vues')[:5]

        return Response({
            'total_articles':  qs.count(),
            'publies':         qs.filter(statut='publie').count(),
            'brouillons':      qs.filter(statut='brouillon').count(),
            'programmes':      qs.filter(statut='programme', date_publication__gt=timezone.now()).count(),
            'categories':      Categorie.objects.count(),
            'tags':            Tag.objects.count(),
            'total_vues':      total_vues,
            'articles_populaires': ArticleListSerializer(top, many=True, context={'request': request}).data,
        })
