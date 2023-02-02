# Generated by Django 3.0.3 on 2020-02-16 13:22
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("config", "0010_auto_20200216_1243")]

    operations = [
        migrations.AddField(
            model_name="bioconfiguration",
            name="bio_pic",
            field=models.ImageField(null=True, upload_to="bio-pic/%Y/%m/%d"),
        ),
        migrations.AddField(
            model_name="bioconfiguration",
            name="pic_0",
            field=models.ImageField(blank=True, upload_to="bio-pic/%Y/%m/%d"),
        ),
        migrations.AddField(
            model_name="bioconfiguration",
            name="pic_1",
            field=models.ImageField(blank=True, upload_to="bio-pic/%Y/%m/%d"),
        ),
        migrations.AddField(
            model_name="bioconfiguration",
            name="pic_2",
            field=models.ImageField(blank=True, upload_to="bio-pic/%Y/%m/%d"),
        ),
    ]
