# Generated by Django 4.2.4 on 2023-08-12 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_container_info_person_delete_infos_info_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='drank',
            field=models.FloatField(default=0),
        ),
    ]
