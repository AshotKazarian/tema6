# Generated by Django 4.2.16 on 2024-11-06 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_alter_favorite_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]