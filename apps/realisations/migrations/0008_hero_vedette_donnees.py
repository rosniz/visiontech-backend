from django.db import migrations

# Met en avant les 4 produits phares dans le Hero de l'accueil (modifiable ensuite depuis l'admin).
# Seules les réalisations existantes dont le titre commence ainsi sont touchées ; aucune n'est créée.
VEDETTES = {
    'VisionFinance': "Le pilotage financier intelligent de votre entreprise.",
    'VisionDocs':    "Les documents, plus simples avec l'IA.",
    'TCF Express':   "Une plateforme complète pour préparer le TCF Canada.",
    'SalemAgro AI':  "L'intelligence artificielle au service de l'agriculture africaine.",
}


def activer(apps, schema_editor):
    Realisation = apps.get_model('realisations', 'Realisation')
    for prefixe, accroche in VEDETTES.items():
        for r in Realisation.objects.filter(titre__istartswith=prefixe):
            r.en_vedette = True
            if not r.accroche:
                r.accroche = accroche
            r.save(update_fields=['en_vedette', 'accroche'])


def desactiver(apps, schema_editor):
    Realisation = apps.get_model('realisations', 'Realisation')
    Realisation.objects.update(en_vedette=False)


class Migration(migrations.Migration):

    dependencies = [
        ('realisations', '0007_hero_vedette'),
    ]

    operations = [
        migrations.RunPython(activer, desactiver),
    ]
