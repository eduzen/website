# Generated by Django 2.2.7 on 2019-11-12 10:22
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("config", "0008_auto_20180225_1923")]

    operations = [
        migrations.AlterField(
            model_name="bioconfiguration",
            name="subtitle",
            field=models.CharField(blank=True, default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="contactconfiguration",
            name="subtitle",
            field=models.CharField(blank=True, default="", max_length=255),
            preserve_default=False,
        ),
    ]