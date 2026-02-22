from apps.services.models import Service

print("🚀 Peuplement des services VisionTech...")

# Supprimer les services existants (optionnel)
# Service.objects.all().delete()

# 1. Développement de Sites Web
Service.objects.create(
    nom="Développement de Sites Web",
    description_courte="Sites web modernes, responsives et performants pour votre entreprise",
    description="""Nous créons des sites web professionnels qui reflètent votre identité et atteignent vos objectifs. Que ce soit pour une vitrine, un site e-commerce, ou un portail d'entreprise, nous utilisons les dernières technologies pour garantir performance et expérience utilisateur optimale.""",
    points_forts=[
        "Design moderne et responsive",
        "Optimisation SEO",
        "Interface d'administration facile",
        "Performance optimale",
        "Support et maintenance"
    ],
    prix_a_partir_de=500000,
    duree_estimee="3-6 semaines",
    est_actif=True,
    ordre=1
)

# 2. Développement d'Applications Web
Service.objects.create(
    nom="Développement d'Applications Web",
    description_courte="Applications web robustes pour digitaliser vos processus métier",
    description="""Transformez vos processus avec des applications web sur mesure. Nous développons des solutions SaaS, plateformes de gestion, CRM, ERP adaptés à vos besoins. Nos applications sont évolutives, sécurisées et faciles à utiliser.""",
    points_forts=[
        "Architecture scalable",
        "API REST intégrée",
        "Authentification sécurisée",
        "Tableaux de bord analytics",
        "Gestion des rôles et permissions"
    ],
    prix_a_partir_de=1500000,
    duree_estimee="2-4 mois",
    est_actif=True,
    ordre=2
)

# 3. Développement d'Applications Mobile
Service.objects.create(
    nom="Développement d'Applications Mobile",
    description_courte="Applications mobiles natives et multiplateformes pour iOS et Android",
    description="""Atteignez vos utilisateurs sur mobile avec des applications performantes. Nous développons des applications natives ou multiplateformes selon vos besoins. De la conception UX/UI au déploiement sur les stores, nous vous accompagnons à chaque étape.""",
    points_forts=[
        "Design UX/UI adapté mobile",
        "Applications cross-platform",
        "Notifications push",
        "Mode hors-ligne",
        "Publication sur stores"
    ],
    prix_a_partir_de=2000000,
    duree_estimee="2-5 mois",
    est_actif=True,
    ordre=3
)

# 4. Formation du Personnel
Service.objects.create(
    nom="Formation du Personnel en Technologie",
    description_courte="Formations sur mesure pour développer les compétences de vos équipes",
    description="""Boostez les compétences de vos collaborateurs avec nos formations pratiques. Nous proposons des programmes en développement web, mobile, data science, cybersécurité. Nos formations sont personnalisables et disponibles en présentiel ou à distance.""",
    points_forts=[
        "Programmes personnalisés",
        "Formateurs experts",
        "Approche pratique",
        "Présentiel ou à distance",
        "Certificat de réussite"
    ],
    prix_a_partir_de=150000,
    duree_estimee="1-12 semaines",
    est_actif=True,
    ordre=4
)

# 5. Automatisation des Processus
Service.objects.create(
    nom="Automatisation des Processus Métier",
    description_courte="Automatisez vos tâches répétitives et gagnez en productivité",
    description="""Libérez le potentiel de vos équipes en automatisant les tâches chronophages. Nous développons des solutions d'automatisation sur mesure : workflows, robots RPA, intégrations API. Réduisez les erreurs et accélérez vos processus.""",
    points_forts=[
        "Audit de vos processus",
        "Solutions sur mesure",
        "Intégration avec vos outils",
        "Réduction des coûts",
        "ROI rapide"
    ],
    prix_a_partir_de=800000,
    duree_estimee="2-8 semaines",
    est_actif=True,
    ordre=5
)

print(f"✅ {Service.objects.count()} services créés avec succès!")
print("\nServices créés:")
for service in Service.objects.all():
    print(f"  - {service.nom} ({service.prix_a_partir_de:,.0f} FCFA)".replace(',', ' '))
