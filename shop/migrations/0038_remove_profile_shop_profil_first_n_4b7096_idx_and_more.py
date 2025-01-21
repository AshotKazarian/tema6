# Generated by Django 4.2.16 on 2025-01-01 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0037_remove_profile_shop_profil_user_id_42814b_idx_and_more"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="profile",
            name="shop_profil_first_n_4b7096_idx",
        ),
        migrations.AddIndex(
            model_name="profile",
            index=models.Index(fields=["user"], name="shop_profil_user_id_42814b_idx"),
        ),
    ]
