# Generated by Django 4.1.3 on 2022-11-07 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("haunted_auth", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="apikey",
            options={"get_latest_by": "created_at"},
        ),
    ]