# Generated by Django 5.0.2 on 2024-05-02 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("REST", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="street",
            name="crossroad",
            field=models.ManyToManyField(
                blank=True, through="REST.StreetCrossroad", to="REST.crossroad"
            ),
        ),
    ]
