# Generated by Django 4.1.3 on 2022-12-16 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news_portal", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="portaluser",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]