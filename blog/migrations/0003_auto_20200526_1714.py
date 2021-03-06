# Generated by Django 3.0.6 on 2020-05-26 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("snippets", "0001_initial"),
        ("files", "0001_initial"),
        ("blog", "0002_auto_20200523_1753"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="images",
            field=models.ManyToManyField(related_name="post", to="files.PublicImage"),
        ),
        migrations.AddField(
            model_name="post",
            name="snippets",
            field=models.ManyToManyField(related_name="post", to="snippets.Snippet"),
        ),
    ]
