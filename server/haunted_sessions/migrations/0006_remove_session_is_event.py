# Generated by Django 4.1.3 on 2022-11-23 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("haunted_sessions", "0005_alter_session_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="session",
            name="is_event",
        ),
    ]
