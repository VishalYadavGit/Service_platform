# Generated by Django 5.0.1 on 2024-03-14 14:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("service_platform", "0013_merge_0010_merge_20240128_1804_0012_cart_ispaid"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
