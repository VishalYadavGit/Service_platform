# Generated by Django 5.0.1 on 2024-02-13 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_platform', '0011_delete_product_alter_service_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='ispaid',
            field=models.BooleanField(default=False),
        ),
    ]
