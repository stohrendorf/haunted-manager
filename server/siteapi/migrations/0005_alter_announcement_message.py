# Generated by Django 4.2.15 on 2024-08-21 17:34

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("siteapi", "0004_alter_announcement_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="message",
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
