# Generated by Django 4.1.3 on 2022-12-14 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("news_portal", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="portaluser",
            old_name="type",
            new_name="user_type",
        ),
    ]