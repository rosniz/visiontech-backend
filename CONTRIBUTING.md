# 🤝 Guide de contribution - VisionTech API

Merci de votre intérêt pour contribuer à VisionTech API!

## 🚀 Démarrage rapide pour les développeurs

### 1. Fork et clone

```bash
git clone https://github.com/votre-username/visiontech_api.git
cd visiontech_api
```

### 2. Configuration de l'environnement

```bash
cp .env.example .env
# Éditez .env avec vos valeurs
```

### 3. Lancer le projet

```bash
# Avec le script d'initialisation
chmod +x init.sh
./init.sh

# Ou manuellement
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 📝 Standards de code

### Python

- Suivre PEP 8
- Utiliser des docstrings pour toutes les fonctions/classes
- Maximum 100 caractères par ligne
- Utiliser les type hints quand possible

### Django

- Un modèle = une responsabilité
- Utiliser les serializers DRF pour toutes les API
- Toujours ajouter des `verbose_name` en français
- Documenter les ViewSets

### Git

- Branches nommées: `feature/nom-feature` ou `fix/nom-bug`
- Commits en français, clairs et concis
- Un commit = une fonctionnalité ou un fix

### Exemple de commit

```
feat(formations): ajouter filtre par prix

- Ajout du filtrage par prix min/max
- Mise à jour de la documentation Swagger
- Ajout de tests unitaires
```

## 🧪 Tests

### Exécuter les tests

```bash
docker-compose exec web python manage.py test
```

### Écrire des tests

Chaque nouvelle fonctionnalité doit avoir des tests:

```python
from django.test import TestCase
from .models import Formation

class FormationTestCase(TestCase):
    def setUp(self):
        Formation.objects.create(
            titre="Test Formation",
            description="Description test",
            prix=10000
        )
    
    def test_formation_creation(self):
        formation = Formation.objects.get(titre="Test Formation")
        self.assertEqual(formation.prix, 10000)
```

## 📦 Ajouter une nouvelle app

```bash
# Créer l'app
docker-compose exec web python manage.py startapp nouvelle_app apps/nouvelle_app

# Ajouter dans INSTALLED_APPS (core/settings.py)
INSTALLED_APPS = [
    ...
    'apps.nouvelle_app',
]

# Créer le modèle, serializer, viewset, urls
# Faire les migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## 🔄 Workflow de développement

1. **Créer une branche**
```bash
git checkout -b feature/ma-nouvelle-feature
```

2. **Développer et tester**
```bash
# Faire vos modifications
docker-compose exec web python manage.py test
```

3. **Commit**
```bash
git add .
git commit -m "feat(app): description de la feature"
```

4. **Push et Pull Request**
```bash
git push origin feature/ma-nouvelle-feature
# Créer une PR sur GitHub
```

## 📚 Structure d'une app Django

```
apps/nouvelle_app/
├── __init__.py
├── admin.py          # Configuration admin Django
├── apps.py           # Configuration de l'app
├── models.py         # Modèles de données
├── serializers.py    # Serializers DRF
├── views.py          # ViewSets API
├── urls.py           # Routes de l'API
└── tests.py          # Tests unitaires
```

## 🎨 Bonnes pratiques

### Modèles

```python
class MonModele(models.Model):
    """Description claire du modèle"""
    
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom",
        help_text="Nom complet de l'entité"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Mon Modèle"
        verbose_name_plural = "Mes Modèles"
    
    def __str__(self):
        return self.nom
```

### Serializers

```python
class MonSerializer(serializers.ModelSerializer):
    """Serializer pour MonModele"""
    
    # Champs calculés
    url_complete = serializers.SerializerMethodField()
    
    class Meta:
        model = MonModele
        fields = ['id', 'nom', 'url_complete', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_url_complete(self, obj):
        """Retourne l'URL complète"""
        return f"https://example.com/{obj.id}"
```

### ViewSets

```python
class MonViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour MonModele
    
    Liste, créé, récupère, modifie et supprime les instances
    """
    
    queryset = MonModele.objects.all()
    serializer_class = MonSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom']
    ordering_fields = ['created_at', 'nom']
```

## 🐛 Debugging

### Voir les logs

```bash
docker-compose logs -f web
```

### Shell Django

```bash
docker-compose exec web python manage.py shell
```

### Accéder à la base de données

```bash
docker-compose exec db psql -U visiontech_user -d visiontech_db
```

## 📋 Checklist avant Pull Request

- [ ] Le code suit PEP 8
- [ ] Les tests passent
- [ ] La documentation est à jour
- [ ] Les migrations sont créées
- [ ] Pas de secrets dans le code
- [ ] Les fichiers statiques sont collectés
- [ ] Swagger est à jour

## 🆘 Besoin d'aide?

- Consultez README.md et commands.md
- Voir la documentation Django: https://docs.djangoproject.com
- Voir la documentation DRF: https://www.django-rest-framework.org
- Ouvrez une issue sur GitHub

## 📄 Licence

En contribuant, vous acceptez que votre code soit sous licence MIT.

Merci de contribuer à VisionTech API! 🚀
