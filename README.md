# 🚀 VisionTech API

API REST complète pour le site VisionTech développée avec Django Rest Framework, PostgreSQL et Docker.

## 📋 Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Technologies](#technologies)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Documentation Swagger](#documentation-swagger)

## ✨ Fonctionnalités

- ✅ CRUD complet pour Formations, Services, Réalisations et Contact
- ✅ API REST versionnée (v1)
- ✅ Upload d'images via Cloudinary
- ✅ Documentation automatique avec Swagger/OpenAPI
- ✅ PostgreSQL en production
- ✅ Architecture Dockerisée
- ✅ CORS configuré pour https://visiontech.vision
- ✅ Interface d'administration Django
- ✅ Filtrage et recherche avancés

## 🛠 Technologies

- **Backend**: Django 5.0, Django Rest Framework 3.14
- **Base de données**: PostgreSQL 16
- **Stockage images**: Cloudinary
- **Conteneurisation**: Docker & Docker Compose
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Serveur**: Gunicorn

## 📦 Prérequis

- Docker et Docker Compose installés
- Compte Cloudinary (gratuit)
- Git

## 🚀 Installation

### Démarrage rapide (2 minutes)

```bash
# 1. Décompresser le projet
unzip visiontech_api.zip
cd visiontech_api

# 2. Configurer l'environnement
cp .env.example .env
nano .env  # Ajoutez vos identifiants Cloudinary

# 3. Lancer (migrations automatiques)
docker-compose up --build
```

**Ou utilisez le script de démarrage:**

```bash
chmod +x start.sh
./start.sh
```

L'application sera accessible sur http://localhost:8000

**Les migrations et fichiers statiques sont appliqués automatiquement au démarrage!**

### Créer un superutilisateur

```bash
docker-compose exec web python manage.py createsuperuser
```

- **API**: http://localhost:8000/api/v1/
- **Admin**: http://localhost:8000/admin/
- **Swagger**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## ⚙️ Configuration

### Cloudinary

1. Créez un compte sur [Cloudinary](https://cloudinary.com)
2. Récupérez vos identifiants dans le Dashboard
3. Ajoutez-les dans le fichier `.env`

### CORS

Pour autoriser d'autres origines, modifiez `CORS_ALLOWED_ORIGINS` dans `.env` :

```env
CORS_ALLOWED_ORIGINS=https://visiontech.vision,https://www.visiontech.vision,http://localhost:3000
```

## 📖 Utilisation

### Commandes Docker

Voir le fichier [commands.md](commands.md) pour toutes les commandes.

### Exemples d'utilisation de l'API

#### Créer une formation

```bash
curl -X POST http://localhost:8000/api/v1/formations/ \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "Formation Django",
    "description": "Apprenez Django de A à Z",
    "prix": "50000",
    "image": "<upload-via-cloudinary>"
  }'
```

#### Lister toutes les formations

```bash
curl http://localhost:8000/api/v1/formations/
```

#### Rechercher des formations

```bash
curl "http://localhost:8000/api/v1/formations/?search=Django"
```

#### Envoyer un message de contact

```bash
curl -X POST http://localhost:8000/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Jean Dupont",
    "email": "jean@example.com",
    "message": "Je souhaite plus d'informations"
  }'
```

## 🏗 Architecture

```
visiontech_api/
├── core/                      # Configuration principale Django
│   ├── __init__.py
│   ├── settings.py           # Paramètres Django
│   ├── urls.py               # URLs principales
│   ├── wsgi.py
│   └── asgi.py
├── apps/                      # Applications Django
│   ├── formations/           # App formations
│   │   ├── models.py         # Modèle Formation
│   │   ├── serializers.py    # Serializer DRF
│   │   ├── views.py          # ViewSet API
│   │   ├── urls.py
│   │   └── admin.py
│   ├── services/             # App services
│   ├── realisations/         # App réalisations
│   └── contact/              # App contact
├── Dockerfile                 # Image Docker
├── docker-compose.yml         # Orchestration
├── requirements.txt           # Dépendances Python
├── .env.example              # Template variables d'env
├── manage.py
├── README.md
└── commands.md
```

### Modèles de données

#### Formation
- `titre`: CharField
- `description`: TextField
- `image`: CloudinaryField
- `prix`: DecimalField
- `created_at`: DateTimeField

#### Service
- `nom`: CharField
- `description`: TextField
- `image`: CloudinaryField
- `created_at`: DateTimeField

#### Realisation
- `titre`: CharField
- `description`: TextField
- `image`: CloudinaryField
- `lien`: URLField (optionnel)
- `created_at`: DateTimeField

#### Contact
- `nom`: CharField
- `email`: EmailField
- `message`: TextField
- `date`: DateTimeField
- `lu`: BooleanField

## 🔗 API Endpoints

### Formations
- `GET /api/v1/formations/` - Liste toutes les formations
- `POST /api/v1/formations/` - Créer une formation
- `GET /api/v1/formations/{id}/` - Détails d'une formation
- `PUT /api/v1/formations/{id}/` - Modifier une formation
- `PATCH /api/v1/formations/{id}/` - Modification partielle
- `DELETE /api/v1/formations/{id}/` - Supprimer une formation

### Services
- `GET /api/v1/services/` - Liste tous les services
- `POST /api/v1/services/` - Créer un service
- `GET /api/v1/services/{id}/` - Détails d'un service
- `PUT /api/v1/services/{id}/` - Modifier un service
- `PATCH /api/v1/services/{id}/` - Modification partielle
- `DELETE /api/v1/services/{id}/` - Supprimer un service

### Réalisations
- `GET /api/v1/realisations/` - Liste toutes les réalisations
- `POST /api/v1/realisations/` - Créer une réalisation
- `GET /api/v1/realisations/{id}/` - Détails d'une réalisation
- `PUT /api/v1/realisations/{id}/` - Modifier une réalisation
- `PATCH /api/v1/realisations/{id}/` - Modification partielle
- `DELETE /api/v1/realisations/{id}/` - Supprimer une réalisation

### Contact
- `GET /api/v1/contact/` - Liste tous les messages
- `POST /api/v1/contact/` - Envoyer un message
- `GET /api/v1/contact/{id}/` - Détails d'un message
- `PUT /api/v1/contact/{id}/` - Modifier un message
- `DELETE /api/v1/contact/{id}/` - Supprimer un message
- `POST /api/v1/contact/{id}/mark_as_read/` - Marquer comme lu
- `POST /api/v1/contact/{id}/mark_as_unread/` - Marquer comme non lu

### Paramètres de requête disponibles

- `?search=terme` - Recherche textuelle
- `?ordering=field` - Tri (`-field` pour descendant)
- `?page=2` - Pagination
- `?lu=true` - Filtrer les messages lus (Contact uniquement)

## 📚 Documentation Swagger

Accédez à la documentation interactive complète sur :

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

La documentation permet de :
- ✅ Visualiser tous les endpoints
- ✅ Tester directement les requêtes
- ✅ Voir les schémas de données
- ✅ Télécharger la spécification OpenAPI

## 🔒 Sécurité

### En production

1. **Désactiver DEBUG**
```env
DEBUG=False
```

2. **Utiliser une SECRET_KEY forte**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

3. **Configurer ALLOWED_HOSTS**
```env
ALLOWED_HOSTS=visiontech.vision,www.visiontech.vision
```

4. **Utiliser HTTPS**
```python
# Dans settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🐛 Troubleshooting

### Erreur de connexion à la base de données

```bash
# Vérifier que PostgreSQL est démarré
docker-compose ps

# Voir les logs
docker-compose logs db
```

### Erreur Cloudinary

Vérifiez vos identifiants dans `.env` et que votre compte est actif.

### Port 8000 déjà utilisé

```bash
# Modifier le port dans docker-compose.yml
ports:
  - "8001:8000"  # Utiliser 8001 au lieu de 8000
```

## 📝 Licence

MIT

## 👨‍💻 Auteur

VisionTech - API développée avec ❤️ par un ingénieur backend senior

## 🤝 Support

Pour toute question ou problème, contactez : contact@visiontech.vision