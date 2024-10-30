# Generated by Django 4.2.16 on 2024-10-28 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='product',
            name='shop_produc_id_f21274_idx',
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['slug'], name='shop_produc_slug_76971b_idx'),
        ),
    ]