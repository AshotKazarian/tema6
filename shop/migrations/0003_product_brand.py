# Generated by Django 4.1.13 on 2024-10-24 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_brand_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.brand'),
            preserve_default=False,
        ),
    ]