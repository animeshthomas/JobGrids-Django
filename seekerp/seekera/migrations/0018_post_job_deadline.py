# Generated by Django 4.2 on 2023-04-30 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seekera', '0017_alter_review_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post_job',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
