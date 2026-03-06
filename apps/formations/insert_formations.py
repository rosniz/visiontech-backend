"""
Script d'insertion des formations VisionTech
Utilisation : python manage.py shell < insert_formations.py
Ou           : python insert_formations.py (depuis le dossier du projet avec django configuré)
"""

import os
import django

# Décommente si tu exécutes en dehors de manage.py shell
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# django.setup()

from apps.formations.models import Formation

formations_data = [
    {
        "titre": "Expert Développement Web Frontend",
        "sous_titre": "Maîtrisez les technologies modernes du développement web côté client",
        "description_courte": "Devenez expert en développement frontend avec HTML, CSS, JavaScript, React et les outils modernes. Créez des interfaces web performantes, responsives et accessibles.",
        "description_complete": """
Cette formation vous permettra de maîtriser l'ensemble des technologies du développement web frontend moderne.

Vous apprendrez à concevoir et développer des interfaces utilisateur professionnelles avec :
- HTML5 sémantique et accessibilité web
- CSS3 avancé, Flexbox, Grid et animations
- JavaScript ES6+ et programmation asynchrone
- React.js et gestion d'état (Redux, Context API)
- TypeScript pour un code robuste et maintenable
- Vite, Webpack et outils de build modernes
- Tests unitaires et d'intégration (Jest, React Testing Library)
- Déploiement et optimisation des performances

À la fin de la formation, vous serez capable de concevoir et livrer des applications web complètes côté client.
        """.strip(),
        "duree": "4 mois",
        "niveau": "Débutant à Avancé",
        "prix": 250000,
    },
    {
        "titre": "Expert Développement Web Backend",
        "sous_titre": "Concevez des APIs robustes et des architectures serveur scalables",
        "description_courte": "Maîtrisez le développement backend avec Python/Django, les bases de données, les APIs REST et GraphQL. Construisez des systèmes robustes et sécurisés.",
        "description_complete": """
Cette formation vous forme aux métiers du développement backend pour concevoir des systèmes serveurs fiables et scalables.

Au programme :
- Python avancé et bonnes pratiques
- Django et Django REST Framework
- Conception et modélisation de bases de données (PostgreSQL, MySQL)
- APIs REST et GraphQL
- Authentification et sécurité (JWT, OAuth2)
- Docker et containerisation
- CI/CD et déploiement en production
- Architecture microservices
- Optimisation des performances et mise en cache (Redis)

Vous serez autonome pour concevoir, développer et déployer des backends professionnels.
        """.strip(),
        "duree": "4 mois",
        "niveau": "Intermédiaire",
        "prix": 250000,
    },
    {
        "titre": "Expert Développement Web Fullstack",
        "sous_titre": "Maîtrisez l'intégralité du cycle de développement web, du frontend au backend",
        "description_courte": "Formation complète couvrant le développement frontend et backend. Devenez un développeur fullstack capable de concevoir et livrer des applications web de A à Z.",
        "description_complete": """
La formation Fullstack combine les compétences frontend et backend pour former des développeurs polyvalents capables de gérer un projet web dans son intégralité.

Contenu de la formation :
- Fondamentaux HTML, CSS, JavaScript
- React.js pour le frontend
- Python et Django pour le backend
- Bases de données relationnelles et NoSQL
- API REST et intégration frontend/backend
- Gestion de version avec Git et GitHub
- Docker et environnements de développement
- Déploiement sur serveurs cloud (VPS, AWS, Heroku)
- Méthodologies Agile et gestion de projet

Cette formation est idéale pour les personnes souhaitant acquérir une vision complète du développement web.
        """.strip(),
        "duree": "6 mois",
        "niveau": "Débutant à Avancé",
        "prix": 400000,
    },
    {
        "titre": "Expert Marketing Digital",
        "sous_titre": "Stratégies digitales, réseaux sociaux, SEO et publicité en ligne",
        "description_courte": "Maîtrisez les leviers du marketing digital : SEO, SEA, réseaux sociaux, email marketing, content marketing et analytics. Développez des stratégies efficaces pour booster la visibilité en ligne.",
        "description_complete": """
Cette formation vous prépare à devenir un expert du marketing digital capable de concevoir et piloter des stratégies digitales performantes.

Modules couverts :
- Fondamentaux du marketing digital et stratégie omnicanale
- SEO (référencement naturel) : technique, contenu et netlinking
- SEA : Google Ads, Facebook Ads et publicité programmatique
- Community Management et gestion des réseaux sociaux
- Email marketing et marketing automation
- Content Marketing et storytelling de marque
- Google Analytics 4, Tag Manager et reporting
- E-commerce et optimisation des conversions (CRO)
- Influence marketing et relations presse digitale

À l'issue de cette formation, vous saurez élaborer et exécuter des campagnes digitales à fort ROI.
        """.strip(),
        "duree": "3 mois",
        "niveau": "Débutant à Intermédiaire",
        "prix": 180000,
    },
    {
        "titre": "Expert Intelligence Artificielle Appliquée et Automatisation",
        "sous_titre": "Intégrez l'IA et l'automatisation dans vos processus métier",
        "description_courte": "Apprenez à utiliser et intégrer les outils d'IA dans vos workflows professionnels. Automatisez vos processus métier avec des solutions no-code et low-code basées sur l'IA.",
        "description_complete": """
Cette formation pratique vous permet de comprendre et d'exploiter l'intelligence artificielle pour transformer vos méthodes de travail et automatiser vos processus.

Programme :
- Comprendre l'IA : machine learning, deep learning et LLMs
- Outils IA no-code et low-code (Make, Zapier, n8n)
- Intégration des APIs d'IA (OpenAI, Anthropic, Gemini)
- Automatisation des workflows métier
- Chatbots et assistants virtuels personnalisés
- Vision par ordinateur et traitement du langage naturel (NLP)
- IA générative : images, textes, vidéos et audio
- Éthique, biais et gouvernance de l'IA
- Cas d'usage par secteur : santé, finance, marketing, RH

Vous serez capable d'identifier les opportunités d'automatisation et d'intégrer l'IA dans votre organisation.
        """.strip(),
        "duree": "3 mois",
        "niveau": "Débutant à Intermédiaire",
        "prix": 200000,
    },
    {
        "titre": "Expert Data Analyst et Business Intelligence",
        "sous_titre": "Transformez les données en décisions stratégiques avec l'analyse et la BI",
        "description_courte": "Maîtrisez l'analyse de données, la visualisation et la Business Intelligence. Apprenez à collecter, traiter et interpréter les données pour guider les décisions business.",
        "description_complete": """
Cette formation vous forme à l'analyse de données et à la Business Intelligence pour transformer les données brutes en insights actionnables.

Contenu :
- Fondamentaux de la data analyse et statistiques
- SQL avancé pour l'extraction et manipulation de données
- Python pour la data analyse (Pandas, NumPy, Matplotlib, Seaborn)
- Power BI : dashboards interactifs et rapports professionnels
- Tableau et outils de visualisation de données
- Modélisation des données et data warehousing
- ETL (Extract, Transform, Load) et pipelines de données
- KPIs, métriques et reporting métier
- Machine Learning appliqué à l'analyse prédictive
- Google Looker Studio et intégration Google Analytics

À la fin de la formation, vous serez capable de concevoir des tableaux de bord et des rapports d'analyse pour la prise de décision.
        """.strip(),
        "duree": "4 mois",
        "niveau": "Intermédiaire",
        "prix": 220000,
    },
    {
        "titre": "Prompt Engineering et Outils IA",
        "sous_titre": "Maîtrisez l'art de communiquer avec les modèles d'IA pour des résultats optimaux",
        "description_courte": "Apprenez les techniques de prompt engineering pour tirer le meilleur des modèles d'IA. Maîtrisez ChatGPT, Claude, Midjourney et les principaux outils IA du marché.",
        "description_complete": """
Cette formation pratique vous apprend à maîtriser les modèles d'IA générative et à rédiger des prompts efficaces pour obtenir des résultats professionnels.

Programme :
- Comprendre le fonctionnement des LLMs (GPT, Claude, Gemini, Llama)
- Techniques de prompt engineering : zero-shot, few-shot, chain-of-thought
- Prompts avancés : rôles, contraintes, formats de sortie
- ChatGPT et GPT-4 : cas d'usage professionnels
- Claude d'Anthropic : rédaction, analyse et code
- Midjourney, DALL-E et Stable Diffusion pour la création visuelle
- Outils IA pour la productivité (Notion AI, Copilot, Perplexity)
- Création d'agents IA et workflows automatisés
- Évaluation et amélioration itérative des prompts
- Cas pratiques par métier : marketing, dev, RH, finance

Vous ressortirez capable d'exploiter pleinement les outils IA dans votre activité professionnelle quotidienne.
        """.strip(),
        "duree": "6 semaines",
        "niveau": "Tous niveaux",
        "prix": 120000,
    },
]


def insert_formations():
    created_count = 0
    updated_count = 0

    for data in formations_data:
        formation, created = Formation.objects.update_or_create(
            titre=data["titre"],
            defaults=data
        )
        if created:
            created_count += 1
            print(f"✅ Créée  : {formation.titre}")
        else:
            updated_count += 1
            print(f"🔄 Mise à jour : {formation.titre}")

    print(f"\n📊 Résultat : {created_count} créées, {updated_count} mises à jour")
    print(f"📚 Total formations en base : {Formation.objects.count()}")


if __name__ == "__main__":
    insert_formations()