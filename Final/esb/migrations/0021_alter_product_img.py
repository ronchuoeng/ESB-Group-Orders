# Generated by Django 4.1.2 on 2023-02-22 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("esb", "0020_rename_quantity_purchaseorder_target_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="img",
            field=models.ImageField(upload_to="esb/static/esb/image"),
        ),
    ]
