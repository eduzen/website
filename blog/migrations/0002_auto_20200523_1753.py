# Generated by Django 3.0.6 on 2020-05-23 20:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_squashed_0012_auto_20200521_1246"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="pompadour",
            field=models.CharField(blank=True, max_length=800, verbose_name="Resumen para portada"),
        ),
    ]
