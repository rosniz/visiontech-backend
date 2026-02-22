#!/bin/bash

echo "🚀 Déploiement VisionTech API"
echo "=============================="

# Vérifier si on est en production
read -p "Êtes-vous sûr de vouloir déployer en PRODUCTION? (yes/no) " -r
echo
if [[ ! $REPLY =~ ^yes$ ]]; then
    echo "Déploiement annulé."
    exit 1
fi

# Sauvegarder la base de données
echo "💾 Sauvegarde de la base de données..."
docker-compose exec db pg_dump -U visiontech_user visiontech_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Récupérer les dernières modifications
echo "📥 Récupération des dernières modifications..."
git pull origin main

# Arrêter les conteneurs
echo "🛑 Arrêt des conteneurs..."
docker-compose -f docker-compose.prod.yml down

# Reconstruire les images
echo "🔨 Reconstruction des images..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Démarrer les conteneurs
echo "🚀 Démarrage des conteneurs..."
docker-compose -f docker-compose.prod.yml up -d

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente du démarrage de PostgreSQL..."
sleep 15

# Appliquer les migrations
echo "📊 Application des migrations..."
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Vérifier le déploiement
echo "🔍 Vérification du déploiement..."
docker-compose -f docker-compose.prod.yml exec web python manage.py check --deploy

echo ""
echo "✅ Déploiement terminé!"
echo ""
echo "📊 Statut des conteneurs:"
docker-compose -f docker-compose.prod.yml ps
echo ""
echo "📝 Pour voir les logs: docker-compose -f docker-compose.prod.yml logs -f"
