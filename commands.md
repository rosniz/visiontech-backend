# 📝 Commandes Docker pour VisionTech API

## 🚀 Démarrage rapide

### Première installation

```bash
# 1. Copier le fichier d'environnement
cp .env.example .env

# 2. Éditer .env avec vos valeurs
nano .env

# 3. Construire les images Docker
docker-compose build

# 4. Démarrer les conteneurs
docker-compose up -d

# 5. Appliquer les migrations
docker-compose exec web python manage.py migrate

# 6. Créer un superutilisateur
docker-compose exec web python manage.py createsuperuser

# 7. Collecter les fichiers statiques
docker-compose exec web python manage.py collectstatic --noinput
```

## 🔧 Gestion des conteneurs

### Démarrer les services

```bash
# Démarrer en mode détaché (arrière-plan)
docker-compose up -d

# Démarrer en mode interactif (voir les logs)
docker-compose up

# Démarrer un service spécifique
docker-compose up -d db
docker-compose up -d web
```

### Arrêter les services

```bash
# Arrêter tous les conteneurs
docker-compose stop

# Arrêter et supprimer les conteneurs
docker-compose down

# Arrêter et supprimer conteneurs + volumes
docker-compose down -v
```

### Redémarrer les services

```bash
# Redémarrer tous les services
docker-compose restart

# Redémarrer un service spécifique
docker-compose restart web
docker-compose restart db
```

### Reconstruire les images

```bash
# Reconstruire toutes les images
docker-compose build

# Reconstruire sans cache
docker-compose build --no-cache

# Reconstruire et redémarrer
docker-compose up -d --build
```

## 📊 Gestion de la base de données

### Migrations

```bash
# Créer de nouvelles migrations
docker-compose exec web python manage.py makemigrations

# Appliquer les migrations
docker-compose exec web python manage.py migrate

# Voir l'état des migrations
docker-compose exec web python manage.py showmigrations

# Annuler une migration
docker-compose exec web python manage.py migrate <app_name> <migration_name>
```

### Backup et restauration

```bash
# Créer un backup de la base de données
docker-compose exec db pg_dump -U visiontech_user visiontech_db > backup.sql

# Restaurer une base de données
docker-compose exec -T db psql -U visiontech_user visiontech_db < backup.sql

# Backup avec compression
docker-compose exec db pg_dump -U visiontech_user visiontech_db | gzip > backup.sql.gz
```

### Accès direct à PostgreSQL

```bash
# Se connecter à PostgreSQL
docker-compose exec db psql -U visiontech_user -d visiontech_db

# Commandes PostgreSQL utiles:
# \l              - Lister les bases de données
# \dt             - Lister les tables
# \d <table>      - Décrire une table
# \q              - Quitter
```

## 👤 Gestion des utilisateurs

```bash
# Créer un superutilisateur
docker-compose exec web python manage.py createsuperuser

# Créer un superutilisateur en mode non-interactif
docker-compose exec web python manage.py createsuperuser \
  --noinput \
  --username admin \
  --email admin@visiontech.vision

# Changer le mot de passe d'un utilisateur
docker-compose exec web python manage.py changepassword <username>
```

## 🗂 Gestion des fichiers statiques

```bash
# Collecter les fichiers statiques
docker-compose exec web python manage.py collectstatic --noinput

# Forcer la collecte (écraser les fichiers existants)
docker-compose exec web python manage.py collectstatic --noinput --clear
```

## 🔍 Logs et débogage

### Voir les logs

```bash
# Voir tous les logs
docker-compose logs

# Suivre les logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs web
docker-compose logs db

# Suivre les logs d'un service
docker-compose logs -f web

# Voir les 100 dernières lignes
docker-compose logs --tail=100 web
```

### Shell Django

```bash
# Ouvrir le shell Django
docker-compose exec web python manage.py shell

# Shell avec imports automatiques
docker-compose exec web python manage.py shell_plus
```

### Shell système

```bash
# Accéder au shell du conteneur web
docker-compose exec web bash

# Accéder au shell du conteneur db
docker-compose exec db bash
```

## 🧪 Tests et qualité du code

```bash
# Exécuter les tests
docker-compose exec web python manage.py test

# Tests avec verbosité
docker-compose exec web python manage.py test --verbosity=2

# Tests d'une app spécifique
docker-compose exec web python manage.py test apps.formations

# Vérifier les problèmes potentiels
docker-compose exec web python manage.py check

# Vérifier la sécurité
docker-compose exec web python manage.py check --deploy
```

## 📦 Gestion des données

### Fixtures (données de test)

```bash
# Créer des fixtures
docker-compose exec web python manage.py dumpdata apps.formations > fixtures/formations.json

# Charger des fixtures
docker-compose exec web python manage.py loaddata fixtures/formations.json

# Créer des fixtures pour toutes les apps
docker-compose exec web python manage.py dumpdata --indent=2 > fixtures/all_data.json
```

### Vider la base de données

```bash
# Supprimer toutes les données (attention!)
docker-compose exec web python manage.py flush

# Supprimer les données d'une app spécifique
docker-compose exec db psql -U visiontech_user -d visiontech_db -c "TRUNCATE TABLE formations_formation CASCADE;"
```

## 🌐 Commandes réseau

```bash
# Voir les ports utilisés
docker-compose ps

# Inspecter le réseau
docker network ls
docker network inspect visiontech_api_default
```

## 🔧 Maintenance

### Nettoyer Docker

```bash
# Supprimer les conteneurs arrêtés
docker container prune

# Supprimer les images inutilisées
docker image prune

# Supprimer les volumes non utilisés
docker volume prune

# Nettoyage complet (ATTENTION: supprime tout ce qui n'est pas utilisé)
docker system prune -a
```

### Vérifier l'espace disque

```bash
# Voir l'utilisation de l'espace par Docker
docker system df

# Détail de l'utilisation
docker system df -v
```

## 🔐 Variables d'environnement

```bash
# Voir les variables d'environnement d'un conteneur
docker-compose exec web env

# Vérifier une variable spécifique
docker-compose exec web bash -c 'echo $DB_NAME'
```

## 📈 Monitoring

```bash
# Voir l'utilisation des ressources
docker stats

# Voir les processus en cours
docker-compose top

# Informations sur un conteneur
docker inspect visiontech_api_web_1
```

## 🚀 Déploiement en production

```bash
# 1. Construire pour la production
docker-compose -f docker-compose.prod.yml build

# 2. Démarrer en production
docker-compose -f docker-compose.prod.yml up -d

# 3. Collecter les statiques
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# 4. Appliquer les migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

## 🛠 Commandes utiles de Django

```bash
# Voir toutes les commandes disponibles
docker-compose exec web python manage.py help

# Créer une nouvelle app
docker-compose exec web python manage.py startapp nom_app

# Vérifier la configuration
docker-compose exec web python manage.py diffsettings

# Générer une nouvelle SECRET_KEY
docker-compose exec web python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 🔄 Mises à jour

```bash
# 1. Arrêter les services
docker-compose down

# 2. Récupérer les mises à jour
git pull

# 3. Mettre à jour les dépendances
docker-compose build --no-cache

# 4. Démarrer les services
docker-compose up -d

# 5. Appliquer les migrations
docker-compose exec web python manage.py migrate

# 6. Collecter les statiques
docker-compose exec web python manage.py collectstatic --noinput
```

## ⚡ Raccourcis pratiques

```bash
# Alias à ajouter dans ~/.bashrc ou ~/.zshrc

alias dcu="docker-compose up -d"
alias dcd="docker-compose down"
alias dcr="docker-compose restart"
alias dcl="docker-compose logs -f"
alias dcps="docker-compose ps"
alias dce="docker-compose exec web"
alias dcm="docker-compose exec web python manage.py"
alias dcsh="docker-compose exec web python manage.py shell"
alias dcmig="docker-compose exec web python manage.py migrate"
alias dcmake="docker-compose exec web python manage.py makemigrations"

# Utilisation:
# dcm createsuperuser
# dcmig
# dcmake
```

## 📝 Notes importantes

- Toujours sauvegarder la base de données avant des opérations destructives
- Utiliser `docker-compose logs -f` pour déboguer les problèmes
- Les fichiers uploadés via Cloudinary ne sont pas stockés localement
- Les volumes Docker persistent les données de PostgreSQL
- En production, utilisez `DEBUG=False` dans `.env`
