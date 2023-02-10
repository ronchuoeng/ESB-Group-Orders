# Generated by Django 4.1.2 on 2023-02-10 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("esb", "0005_alter_category_options_alter_purchases_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ["type", "title"],
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["-active", "title"]},
        ),
        migrations.RenameField(
            model_name="purchases",
            old_name="order_id",
            new_name="quantity",
        ),
        migrations.RemoveField(
            model_name="purchases",
            name="item",
        ),
        migrations.AddField(
            model_name="purchases",
            name="product",
            field=models.ForeignKey(
                default=123,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="esb.product",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="category",
            name="type",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
