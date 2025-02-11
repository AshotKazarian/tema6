# Generated by Django 4.2.16 on 2024-12-28 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0027_remove_comment_email"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ["created"],
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.AlterField(
            model_name="historicalproduct",
            name="country",
            field=models.CharField(
                choices=[
                    ("RU", "Россия"),
                    ("GE", "Германия"),
                    ("JP", "Япония"),
                    ("ND", "Нет данных"),
                ],
                default="ND",
                max_length=2,
                verbose_name="Страна производства",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="country",
            field=models.CharField(
                choices=[
                    ("RU", "Россия"),
                    ("GE", "Германия"),
                    ("JP", "Япония"),
                    ("ND", "Нет данных"),
                ],
                default="ND",
                max_length=2,
                verbose_name="Страна производства",
            ),
        ),
    ]
