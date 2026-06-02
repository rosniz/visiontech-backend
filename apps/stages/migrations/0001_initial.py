import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DemandeStage',
            fields=[
                ('id',                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user',                  models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='demandes_stage', to=settings.AUTH_USER_MODEL, verbose_name='Compte')),
                ('nom',                   models.CharField(max_length=100, verbose_name='Nom')),
                ('prenom',                models.CharField(max_length=100, verbose_name='Prénom')),
                ('telephone',             models.CharField(max_length=25, verbose_name='Téléphone')),
                ('email_contact',         models.EmailField(verbose_name='Email de contact')),
                ('type_stage',            models.CharField(choices=[('vacances','Stage de vacances'),('pre_emploi','Pré-emploi'),('perfectionnement','Perfectionnement')], max_length=20, verbose_name='Type de stage')),
                ('domaine',               models.CharField(blank=True, choices=[('dev_web','Développement Web'),('dev_mobile','Développement Mobile'),('ia_data','IA & Data Science'),('marketing','Marketing Digital'),('design','Design UX/UI'),('autre','Autre')], max_length=20, verbose_name='Domaine souhaité')),
                ('date_debut',            models.DateField(blank=True, null=True, verbose_name='Date de début souhaitée')),
                ('date_fin',              models.DateField(blank=True, null=True, verbose_name='Date de fin souhaitée')),
                ('lettre_motivation',     models.TextField(verbose_name='Lettre de motivation')),
                ('cni_recto',             models.ImageField(blank=True, null=True, upload_to='stages/cni/', verbose_name='CNI recto')),
                ('cni_verso',             models.ImageField(blank=True, null=True, upload_to='stages/cni/', verbose_name='CNI verso')),
                ('carte_etudiant',        models.ImageField(blank=True, null=True, upload_to='stages/docs/', verbose_name='Carte étudiant')),
                ('certificat_scolarite',  models.FileField(blank=True, null=True, upload_to='stages/docs/', verbose_name='Certificat de scolarité (PDF)')),
                ('cv',                    models.FileField(blank=True, null=True, upload_to='stages/cv/', verbose_name='CV (PDF)')),
                ('statut',                models.CharField(choices=[('en_attente','En attente'),('en_etude',"En cours d'étude"),('accepte','Accepté'),('refuse','Refusé')], default='en_attente', max_length=20, verbose_name='Statut')),
                ('commentaire_admin',     models.TextField(blank=True, verbose_name='Message pour le candidat')),
                ('created_at',            models.DateTimeField(auto_now_add=True, verbose_name='Date de soumission')),
                ('updated_at',            models.DateTimeField(auto_now=True, verbose_name='Dernière mise à jour')),
            ],
            options={
                'verbose_name': 'Demande de stage',
                'verbose_name_plural': 'Demandes de stage',
                'ordering': ['-created_at'],
            },
        ),
    ]
