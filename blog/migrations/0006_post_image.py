# Generated by Django 1.11.4 on 2017-10-01 03:36
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("blog", "0005_auto_20170806_2313")]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="post-img/%Y/%m/%d"),
        )
    ]
