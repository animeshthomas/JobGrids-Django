# Generated by Django 4.2 on 2023-04-16 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seekera', '0013_job_providers_usertype_job_seekers_usertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='provider',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='seekera.job_providers'),
        ),
    ]
