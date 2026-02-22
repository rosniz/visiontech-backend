# ⚡ Quick Start - VisionTech API

## Installation automatique en 2 minutes

### Prérequis
- Docker
- Docker Compose

### 🚀 Démarrage (3 commandes seulement)

```bash
# 1. Décompresser et configurer
unzip visiontech_api.zip
cd visiontech_api
cp .env.example .env

# 2. Éditer .env et ajouter vos identifiants Cloudinary
nano .env  # ou vim .env

# 3. Lancer tout automatiquement
docker-compose up --build
```

**C'est tout!** 🎉

Les migrations et la collecte des fichiers statiques se font **automatiquement** au démarrage.

Attendez voir: `Starting development server at http://0.0.0.0:8000/`

### 🎯 Accès à l'application

- **API**: http://localhost:8000/api/v1/
- **Swagger**: http://localhost:8000/swagger/
- **Admin**: http://localhost:8000/admin/

### 👤 Créer un superutilisateur

Dans un nouveau terminal:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 🔍 Voir les logs

```bash
docker-compose logs -f web
```

### 🛑 Arrêter

```bash
docker-compose down
```

### 🔄 Redémarrer

```bash
docker-compose up
```

### ⚠️ En cas de problème

```bash
# Reset complet
docker-compose down -v
docker-compose up --build
```

### 🎯 Accès rapide

| Service | URL |
|---------|-----|
| **API** | http://localhost:8000/api/v1/ |
| **Admin** | http://localhost:8000/admin/ |
| **Swagger** | http://localhost:8000/swagger/ |
| **ReDoc** | http://localhost:8000/redoc/ |

### 🔑 Identifiants Cloudinary

1. Créez un compte sur https://cloudinary.com
2. Dashboard → Account Details
3. Copiez: Cloud Name, API Key, API Secret
4. Collez dans `.env`

### 📝 Commandes essentielles

```bash
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Voir les logs
docker-compose logs -f

# Créer un superuser
docker-compose exec web python manage.py createsuperuser

# Migrations
docker-compose exec web python manage.py migrate
```

### 🧪 Tester l'API

```bash
# Lister les formations
curl http://localhost:8000/api/v1/formations/

# Créer une formation
curl -X POST http://localhost:8000/api/v1/formations/ \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "Formation Django",
    "description": "Apprendre Django",
    "prix": "50000"
  }'
```

### 📚 Documentation complète

- **README.md** - Documentation détaillée
- **commands.md** - Toutes les commandes Docker
- **CONTRIBUTING.md** - Guide de développement

### ⚠️ Important

- Ne commitez JAMAIS le fichier `.env`
- Changez la `SECRET_KEY` en production
- Mettez `DEBUG=False` en production
- Utilisez HTTPS en production

### 🆘 Problèmes?

```bash
# Vérifier l'état des services
docker-compose ps

# Vérifier les logs
docker-compose logs web
docker-compose logs db

# Healthcheck
docker-compose exec web python healthcheck.py
```

### 🎉 Prochaines étapes

1. Connectez-vous à l'admin: http://localhost:8000/admin/
2. Créez des formations, services, réalisations
3. Testez l'API avec Swagger
4. Intégrez avec votre frontend

**Bon développement! 🚀**