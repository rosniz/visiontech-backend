from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandestage',
            name='profil',
            field=models.CharField(
                choices=[
                    ('eleve', 'Élève (Première / Terminale / Bac)'),
                    ('etudiant', 'Étudiant (Validation BTS/HND)'),
                    ('chomeur_travailleur', 'Chômeur / Travailleur'),
                ],
                default='eleve',
                max_length=25,
                verbose_name='Profil',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demandestage',
            name='lettre_responsable',
            field=models.FileField(blank=True, null=True, upload_to='stages/docs/', verbose_name='Lettre du responsable (PDF)'),
        ),
        migrations.AlterField(
            model_name='demandestage',
            name='type_stage',
            field=models.CharField(
                blank=True,
                choices=[
                    ('vacances', 'Stage de vacances'),
                    ('pre_emploi', 'Pré-emploi'),
                    ('perfectionnement', 'Perfectionnement'),
                ],
                max_length=20,
                verbose_name='Type de stage',
            ),
        ),
    ]
