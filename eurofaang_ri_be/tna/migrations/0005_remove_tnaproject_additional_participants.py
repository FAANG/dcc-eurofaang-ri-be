# Generated by Django 5.0.4 on 2024-04-22 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tna', '0004_remove_tnaproject_additional_participants_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tnaproject',
            name='additional_participants',
        ),
    ]