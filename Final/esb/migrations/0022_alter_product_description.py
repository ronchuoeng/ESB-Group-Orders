# Generated by Django 4.1.2 on 2023-02-25 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("esb", "0021_alter_product_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(max_length=1000),
        ),
    ]
