# Generated by Django 4.1.3 on 2022-11-23 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("siteapi", "0003_alter_announcement_message"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="announcement",
            options={"get_latest_by": "created_at", "ordering": ("created_at",)},
        ),
    ]
