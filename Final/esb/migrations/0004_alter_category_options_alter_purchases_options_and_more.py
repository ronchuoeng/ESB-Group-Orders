# Generated by Django 4.1.2 on 2023-02-10 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("esb", "0003_category_alter_product_options_alter_purchases_buyer_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["title"]},
        ),
        migrations.AlterModelOptions(
            name="purchases",
            options={"verbose_name": "Purchases"},
        ),
        migrations.AddField(
            model_name="category",
            name="type",
            field=models.CharField(default=2, max_length=32),
            preserve_default=False,
        ),
    ]
