# Generated by Django 4.1.2 on 2023-02-11 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("esb", "0019_rename_purchases_purchaseorder_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="purchaseorder",
            old_name="quantity",
            new_name="target_quantity",
        ),
    ]