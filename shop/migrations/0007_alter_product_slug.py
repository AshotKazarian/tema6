# Generated by Django 4.2.16 on 2024-10-26 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_remove_product_get_short_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Метка'),
        ),
    ]
