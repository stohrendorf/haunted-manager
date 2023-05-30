# Generated by Django 4.1.3 on 2022-11-03 10:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("haunted_sessions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="session",
            name="players",
            field=models.ManyToManyField(related_name="sessions", to=settings.AUTH_USER_MODEL),
        ),
    ]
