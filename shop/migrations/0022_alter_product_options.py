# Generated by Django 4.2.16 on 2024-12-27 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0021_alter_product_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ["name"],
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
    ]
