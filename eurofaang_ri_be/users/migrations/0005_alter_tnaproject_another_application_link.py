# Generated by Django 5.0.4 on 2024-04-18 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_tnaproject_another_application_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tnaproject',
            name='another_application_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.tnaproject'),
        ),
    ]
