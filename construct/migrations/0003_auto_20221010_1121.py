# Generated by Django 2.0.3 on 2022-10-10 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('construct', '0002_auto_20221010_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='constructionprojects',
            old_name='projectclient',
            new_name='project_client',
        ),
    ]
