from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formations', '0002_remove_formation_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formation',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='formations/'),
        ),
        migrations.AlterField(
            model_name='formation',
            name='syllabus',
            field=models.FileField(blank=True, null=True, upload_to='formations/syllabus/'),
        ),
    ]
