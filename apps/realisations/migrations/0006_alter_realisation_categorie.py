from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realisations', '0005_alter_realisation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realisation',
            name='categorie',
            field=models.CharField(choices=[('developpement', 'Développement Web'), ('mobile', 'Application Mobile'), ('formation', 'Formation & Atelier'), ('conseil', 'Conseil & Stratégie'), ('automatisation', 'IA & Automatisation')], default='developpement', max_length=50, verbose_name='Catégorie'),
        ),
    ]
