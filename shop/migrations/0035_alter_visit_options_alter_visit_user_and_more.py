# Generated by Django 4.2.16 on 2024-12-30 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0034_alter_visit_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="visit",
            options={
                "ordering": ["-visit_time"],
                "verbose_name": "Логирование посещений",
                "verbose_name_plural": "Логирование посещений",
            },
        ),
        migrations.AlterField(
            model_name="visit",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Имя пользователя",
            ),
        ),
        migrations.AlterField(
            model_name="visit",
            name="visit_time",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Время посещения"
            ),
        ),
        migrations.AlterField(
            model_name="visit",
            name="visit_url",
            field=models.CharField(max_length=255, verbose_name="Страница"),
        ),
        migrations.AddIndex(
            model_name="visit",
            index=models.Index(
                fields=["-visit_time"], name="shop_visit_visit_t_204577_idx"
            ),
        ),
    ]
