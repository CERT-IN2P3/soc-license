# Generated by Django 4.2.3 on 2023-08-15 15:34

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Diploma",
            fields=[
                (
                    "uuid",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("private_key", models.CharField(default="", max_length=15000)),
                ("sha512sum", models.CharField(max_length=100)),
            ],
        ),
    ]