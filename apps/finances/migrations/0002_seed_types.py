from django.db import migrations

DEFAULT_TYPES = [
    ('exploitation', "Achats de marchandises / matières premières"),
    ('exploitation', 'Loyers et charges locatives'),
    ('exploitation', 'Énergie (eau, électricité)'),
    ('exploitation', 'Entretien et réparations'),
    ('exploitation', 'Publicité et marketing'),
    ('exploitation', 'Assurances'),
    ('exploitation', 'Dotations aux amortissements'),
    ('exploitation', 'Fournitures de bureau'),

    ('fiscale', 'Impôt sur les sociétés (IS)'),
    ('fiscale', 'TVA non récupérable'),
    ('fiscale', 'Taxe foncière'),
    ('fiscale', 'Contribution économique territoriale'),
    ('fiscale', 'Taxe sur les véhicules de société'),
    ('fiscale', 'Droits de douane'),

    ('personnel', 'Salaires bruts'),
    ('personnel', 'Charges sociales patronales'),
    ('personnel', 'Primes et avantages en nature'),
    ('personnel', 'Formation professionnelle'),

    ('financiere', "Intérêts d'emprunt"),
    ('financiere', 'Agios bancaires'),
    ('financiere', 'Pertes de change'),
    ('financiere', 'Escomptes accordés'),
]


def seed_types(apps, schema_editor):
    TypeCharge = apps.get_model('finances', 'TypeCharge')
    for categorie, nom in DEFAULT_TYPES:
        TypeCharge.objects.get_or_create(categorie=categorie, nom=nom)


def unseed_types(apps, schema_editor):
    TypeCharge = apps.get_model('finances', 'TypeCharge')
    noms = [nom for _, nom in DEFAULT_TYPES]
    TypeCharge.objects.filter(nom__in=noms).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_types, unseed_types),
    ]
