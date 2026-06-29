from django.conf import settings
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from .models import Article

FRONTEND_URL = getattr(settings, 'FRONTEND_URL', 'https://visiontech.vision')


class ArticlesRSSFeed(Feed):
    title = 'VisionTech SARL — Blog'
    link = f'{FRONTEND_URL}/blog'
    description = "Articles, actualités et ressources de VisionTech SARL : développement web, IA, formations."

    def items(self):
        return Article.objects.publies().order_by('-date_publication')[:30]

    def item_title(self, item):
        return item.titre

    def item_description(self, item):
        return item.extrait

    def item_link(self, item):
        return f'{FRONTEND_URL}/blog/{item.slug}'

    def item_pubdate(self, item):
        return item.date_publication

    def item_author_name(self, item):
        return item.auteur_nom

    def item_categories(self, item):
        return [item.categorie.nom] if item.categorie else []


class ArticlesAtomFeed(ArticlesRSSFeed):
    feed_type = Atom1Feed
    subtitle = ArticlesRSSFeed.description
