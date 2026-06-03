from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='telephone',
            field=models.CharField(blank=True, max_length=25, verbose_name='Téléphone'),
        ),
        migrations.AddField(
            model_name='contact',
            name='sujet',
            field=models.CharField(blank=True, max_length=200, verbose_name='Sujet'),
        ),
    ]
