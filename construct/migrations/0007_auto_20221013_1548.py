# Generated by Django 2.0.3 on 2022-10-13 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construct', '0006_auto_20221013_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]
