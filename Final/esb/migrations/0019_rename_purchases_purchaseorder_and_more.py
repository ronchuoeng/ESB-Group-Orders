# Generated by Django 4.1.2 on 2023-02-11 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("esb", "0018_remove_purchases_buyer"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Purchases",
            new_name="PurchaseOrder",
        ),
        migrations.AlterModelOptions(
            name="purchaseorder",
            options={},
        ),
    ]
