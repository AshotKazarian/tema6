# Generated by Django 4.2.16 on 2024-12-29 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0030_delete_profilecomment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="comment_images/"),
        ),
        migrations.AddField(
            model_name="historicalproduct",
            name="file",
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="historicalproduct",
            name="url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="product_files/"),
        ),
        migrations.AddField(
            model_name="product",
            name="url",
            field=models.URLField(blank=True, null=True),
        ),
    ]