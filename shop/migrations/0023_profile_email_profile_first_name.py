# Generated by Django 4.2.16 on 2024-12-27 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0022_alter_product_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="profile",
            name="first_name",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
