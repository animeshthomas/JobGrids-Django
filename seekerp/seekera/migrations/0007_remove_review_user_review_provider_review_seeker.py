# Generated by Django 4.2 on 2023-04-15 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seekera', '0006_remove_review_rating_remove_review_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AddField(
            model_name='review',
            name='provider',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='seekera.job_providers'),
        ),
        migrations.AddField(
            model_name='review',
            name='seeker',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='seekera.job_seekers'),
        ),
    ]
