from apps.realisations.models import Realisation

Realisation.objects.create(
    titre="TCF Express",
    client="TCF Express Academy",
    description=(
        "Plateforme web complète dédiée à la préparation au TCF Canada, "
        "intégrant des interfaces de passage d'examens blancs en conditions réelles. "
        "L'intelligence artificielle corrige automatiquement les productions écrites "
        "et simule les expressions orales des candidats. "
        "La solution répond pleinement aux besoins de l'académie et a généré "
        "une très forte satisfaction client."
    ),
    technologies="React, TypeScript, Tailwind CSS, Django REST Framework, JWT, Swagger, Docker, Docker Compose",
    lien="https://tcf-express.com",
    statut="termine",
    ordre=1,
)

Realisation.objects.create(
    titre="Sensuela",
    client="Sensuela (Maroc)",
    description=(
        "Site e-commerce spécialisé dans la vente de parfums de luxe authentiques "
        "de grandes marques, livraison partout en Afrique. "
        "La plateforme intègre un système de mapping géographique permettant aux clients "
        "de localiser et contacter directement le fournisseur de leur région."
    ),
    technologies="React, TypeScript, Tailwind CSS, Django REST Framework, JWT, Swagger, Docker, Docker Compose",
    lien="https://sensuela.net",
    statut="termine",
    ordre=2,
)

print("✅ 2 réalisations insérées avec succès.")