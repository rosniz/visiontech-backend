# VISIONTECH Backend API

Backend RESTful API pour le site web de VISIONTECH, construit avec Django REST Framework. Ce projet fournit les endpoints pour gérer les services, formations et réalisations de l'entreprise.

## 🚀 Technologies

- **Framework**: Django 4.2+ & Django REST Framework
- **Base de données**: PostgreSQL
- **Containerisation**: Docker & Docker Compose
- **Serveur**: Gunicorn
- **Déploiement**: Render
- **Documentation API**: drf-yasg (Swagger)

## 📋 Prérequis

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optionnel mais recommandé)
- Git

## 🏗️ Structure du Projet

```
visiontech-backend/
├── apps/
│   ├── services/          # Gestion des services offerts
│   ├── formations/        # Gestion des formations
│   └── realisations/      # Gestion du portfolio/réalisations
├── config/
│   ├── settings/          # Configurations (base, dev, prod)
│   ├── urls.py           # Routes principales
│   └── wsgi.py           # Configuration WSGI
├── docker/
│   ├── Dockerfile        # Image Docker
│   └── docker-compose.yml # Orchestration des services
├── requirements/
│   ├── base.txt          # Dépendances de base
│   ├── development.txt   # Dépendances de développement
│   └── production.txt    # Dépendances de production
├── media/                # Fichiers uploadés
├── static/               # Fichiers statiques
├── .env.example          # Template des variables d'environnement
├── .gitignore           # Fichiers à ignorer par Git
├── manage.py            # Script de gestion Django
├── README.md            # Ce fichier
└── render.yaml          # Configuration pour Render
```

## 🛠️ Installation

### Option 1: Avec Docker (Recommandé)

1. **Cloner le repository**
```bash
git clone https://github.com/rosniz/visiontech-backend.git
cd visiontech-backend
```

2. **Créer le fichier .env**
```bash
cp .env.example .env
# Éditer .env avec vos valeurs
```

3. **Lancer avec Docker Compose**
```bash
cd docker
docker-compose up --build
```

4. **Créer un superutilisateur**
```bash
docker-compose exec web python manage.py createsuperuser
```

L'API sera accessible sur `http://localhost:8000`

### Option 2: Installation Locale

1. **Cloner le repository**
```bash
git clone https://github.com/rosniz/visiontech-backend.git
cd visiontech-backend
```

2. **Créer et activer l'environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements/development.txt
```

4. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos valeurs
```

5. **Créer la base de données PostgreSQL**
```bash
createdb visiontech_db
```

6. **Appliquer les migrations**
```bash
python manage.py migrate
```

7. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

8. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

L'API sera accessible sur `http://localhost:8000`

## 📚 API Endpoints

### Services
- `GET /api/services/` - Liste tous les services
- `POST /api/services/` - Créer un nouveau service
- `GET /api/services/{id}/` - Détails d'un service
- `PUT /api/services/{id}/` - Mettre à jour un service
- `DELETE /api/services/{id}/` - Supprimer un service

### Formations
- `GET /api/formations/` - Liste toutes les formations
- `POST /api/formations/` - Créer une nouvelle formation
- `GET /api/formations/{id}/` - Détails d'une formation
- `PUT /api/formations/{id}/` - Mettre à jour une formation
- `DELETE /api/formations/{id}/` - Supprimer une formation

### Réalisations
- `GET /api/realisations/` - Liste toutes les réalisations
- `POST /api/realisations/` - Créer une nouvelle réalisation
- `GET /api/realisations/{id}/` - Détails d'une réalisation
- `PUT /api/realisations/{id}/` - Mettre à jour une réalisation
- `DELETE /api/realisations/{id}/` - Supprimer une réalisation

## 📖 Documentation API

La documentation interactive Swagger est disponible à :
- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`

## 🧪 Tests

```bash
# Lancer tous les tests
python manage.py test

# Avec coverage
pytest --cov=apps

# Tests d'une application spécifique
python manage.py test apps.services
```

## 🔧 Commandes Utiles

```bash
# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le shell Django
python manage.py shell

# Vider la base de données
python manage.py flush
```

## 🚢 Déploiement sur Render

1. **Pousser le code sur GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Connecter à Render**
   - Aller sur [render.com](https://render.com)
   - Connecter votre repository GitHub
   - Render détectera automatiquement `render.yaml`

3. **Configurer les variables d'environnement**
   - `SECRET_KEY`: Votre clé secrète Django
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: Votre domaine Render
   - Les autres variables seront configurées automatiquement

4. **Déployer**
   - Render construira et déploiera automatiquement
   - L'URL sera fournie après le déploiement

## 🔐 Variables d'Environnement

Créer un fichier `.env` basé sur `.env.example` :

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://user:password@localhost:5432/visiontech_db

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Conventions de Code

- Suivre PEP 8 pour le style Python
- Utiliser des noms de variables descriptifs en français ou anglais
- Commenter le code complexe
- Écrire des tests pour les nouvelles fonctionnalités

## 🐛 Rapport de Bugs

Pour signaler un bug, créer une issue sur GitHub avec :
- Description du bug
- Étapes pour reproduire
- Comportement attendu vs comportement actuel
- Captures d'écran si applicable

## 📄 Licence

Ce projet est privé et propriétaire de VISIONTECH.

## 👥 Auteurs

- **VISIONTECH Team** - [GitHub](https://github.com/rosniz)

## 📞 Contact

Pour toute question, contactez l'équipe VISIONTECH.

---

**Note**: Ce projet est en cours de développement actif. Les fonctionnalités peuvent changer.