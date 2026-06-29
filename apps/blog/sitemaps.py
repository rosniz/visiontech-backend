from django.conf import settings
from django.contrib.sitemaps import Sitemap
from .models import Article

FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'https://visiontech.vision')


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority   = 0.7
    protocol   = 'https'

    def items(self):
        return Article.objects.publies()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # URL absolue vers le frontend (Netlify), pas vers l'API — Django la garde telle quelle
        return f'{FRONTEND_URL}/blog/{obj.slug}'
