# Generated by Django 4.2.5 on 2023-09-08 15:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0006_remove_post_images_remove_post_snippets_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="suggestions",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
