# Generated by Django 4.2.16 on 2024-12-28 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0026_remove_profile_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="email",
        ),
    ]