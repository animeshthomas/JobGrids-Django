# Generated by Django 4.2 on 2023-04-15 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seekera', '0008_alter_review_provider_alter_review_seeker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='provider',
        ),
    ]
