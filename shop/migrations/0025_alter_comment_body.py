# Generated by Django 4.2.16 on 2024-12-28 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0024_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="body",
            field=models.TextField(verbose_name=""),
        ),
    ]
