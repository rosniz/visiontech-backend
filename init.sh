#!/bin/bash

echo "🚀 Initialisation de VisionTech API"
echo "===================================="

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si .env existe
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env
    echo "⚠️  N'oubliez pas de configurer vos variables dans .env"
    echo "   Particulièrement les identifiants Cloudinary!"
    read -p "Appuyez sur Entrée pour continuer..."
fi

# Construire les images
echo "🔨 Construction des images Docker..."
docker-compose build

# Démarrer les conteneurs
echo "🐳 Démarrage des conteneurs..."
docker-compose up -d

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente du démarrage de PostgreSQL..."
sleep 10

# Appliquer les migrations
echo "📊 Application des migrations..."
docker-compose exec web python manage.py migrate

# Demander si l'utilisateur veut créer un superuser
echo ""
read -p "Voulez-vous créer un superutilisateur maintenant? (o/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Oo]$ ]]; then
    docker-compose exec web python manage.py createsuperuser
fi

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
docker-compose exec web python manage.py collectstatic --noinput

echo ""
echo "✅ Installation terminée!"
echo ""
echo "🌐 Accès à l'application:"
echo "   - API:         http://localhost:8000/api/v1/"
echo "   - Admin:       http://localhost:8000/admin/"
echo "   - Swagger:     http://localhost:8000/swagger/"
echo "   - ReDoc:       http://localhost:8000/redoc/"
echo ""
echo "📚 Pour plus de commandes, consultez commands.md"
