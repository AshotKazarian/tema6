# Generated by Django 4.2.16 on 2024-12-29 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0031_comment_image_historicalproduct_file_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="comment_images/",
                verbose_name="Изображение",
            ),
        ),
    ]
