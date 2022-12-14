# Generated by Django 4.1.3 on 2022-12-14 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("news_portal", "0002_rename_type_portaluser_user_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="news_portal.reporter"
            ),
        ),
    ]