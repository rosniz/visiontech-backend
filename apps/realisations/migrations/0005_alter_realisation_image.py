from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realisations', '0004_alter_realisation_categorie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realisation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='realisations/'),
        ),
    ]
