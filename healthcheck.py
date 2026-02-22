#!/usr/bin/env python
"""
Script de healthcheck pour VisionTech API
Vérifie que tous les services fonctionnent correctement
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from django.core.exceptions import ImproperlyConfigured
import cloudinary


def check_database():
    """Vérifie la connexion à la base de données"""
    try:
        connection.ensure_connection()
        print("✅ Base de données: OK")
        return True
    except Exception as e:
        print(f"❌ Base de données: ERREUR - {e}")
        return False


def check_cloudinary():
    """Vérifie la configuration Cloudinary"""
    try:
        config = cloudinary.config()
        if config.cloud_name and config.api_key and config.api_secret:
            print("✅ Cloudinary: OK")
            return True
        else:
            print("❌ Cloudinary: Configuration incomplète")
            return False
    except Exception as e:
        print(f"❌ Cloudinary: ERREUR - {e}")
        return False


def check_apps():
    """Vérifie que toutes les apps sont chargées"""
    from django.apps import apps
    try:
        required_apps = [
            'apps.formations',
            'apps.services',
            'apps.realisations',
            'apps.contact'
        ]
        for app_name in required_apps:
            if not apps.is_installed(app_name):
                print(f"❌ App {app_name}: NON INSTALLÉE")
                return False
        print("✅ Applications Django: OK")
        return True
    except Exception as e:
        print(f"❌ Applications: ERREUR - {e}")
        return False


def main():
    """Fonction principale de healthcheck"""
    print("🏥 VisionTech API - Healthcheck")
    print("=" * 40)
    
    checks = [
        check_database(),
        check_cloudinary(),
        check_apps()
    ]
    
    print("=" * 40)
    
    if all(checks):
        print("✅ Tous les services fonctionnent correctement!")
        sys.exit(0)
    else:
        print("❌ Certains services ne fonctionnent pas correctement")
        sys.exit(1)


if __name__ == "__main__":
    main()
