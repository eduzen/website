# Generated by Django 4.1.5 on 2023-01-29 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_auto_20200526_1714"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tag",
            options={"verbose_name": "tag", "verbose_name_plural": "tags"},
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(null=True, verbose_name="slug"),
        ),
        migrations.AlterField(
            model_name="tag",
            name="word",
            field=models.CharField(max_length=50, unique=True, verbose_name="word"),
        ),
    ]
