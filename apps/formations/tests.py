from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Formation


class FormationModelTestCase(TestCase):
    """Tests pour le modèle Formation"""
    
    def setUp(self):
        self.formation = Formation.objects.create(
            titre="Django Avancé",
            description="Formation complète sur Django",
            prix=Decimal("50000.00")
        )
    
    def test_formation_creation(self):
        """Test de création d'une formation"""
        self.assertEqual(self.formation.titre, "Django Avancé")
        self.assertEqual(self.formation.prix, Decimal("50000.00"))
    
    def test_formation_str(self):
        """Test de la représentation string"""
        self.assertEqual(str(self.formation), "Django Avancé")


class FormationAPITestCase(APITestCase):
    """Tests pour l'API Formation"""
    
    def setUp(self):
        self.formation = Formation.objects.create(
            titre="Python Débutant",
            description="Apprendre Python de zéro",
            prix=Decimal("30000.00")
        )
        self.url = '/api/v1/formations/'
    
    def test_get_formations_list(self):
        """Test de récupération de la liste des formations"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_formation_detail(self):
        """Test de récupération d'une formation spécifique"""
        url = f'{self.url}{self.formation.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titre'], "Python Débutant")
    
    def test_create_formation(self):
        """Test de création d'une formation"""
        data = {
            'titre': 'React JS',
            'description': 'Maîtriser React',
            'prix': '40000.00'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Formation.objects.count(), 2)
    
    def test_search_formations(self):
        """Test de recherche de formations"""
        url = f'{self.url}?search=Python'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
