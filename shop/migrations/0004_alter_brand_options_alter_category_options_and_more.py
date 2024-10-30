# Generated by Django 4.2.16 on 2024-10-25 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_brand'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ['name'], 'verbose_name': 'Бренд', 'verbose_name_plural': 'Бренды'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
