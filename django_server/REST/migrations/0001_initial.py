# Generated by Django 5.0.2 on 2024-04-25 18:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Crossroad",
            fields=[
                (
                    "name",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("latitude", models.FloatField(default=0)),
                ("longitude", models.FloatField(default=0)),
                ("cars_count", models.CharField(default="0,0,0,0", max_length=100)),
                ("last_send", models.DateTimeField(blank=True, null=True)),
                ("creation_date", models.DateTimeField(auto_now_add=True, null=True)),
                ("traffic_level", models.FloatField(default=0)),
                ("active", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Street",
            fields=[
                (
                    "name",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("length", models.IntegerField(default=100)),
                ("alert", models.BooleanField(default=False)),
                ("Crossroad", models.ManyToManyField(blank=True, to="REST.crossroad")),
            ],
        ),
        migrations.CreateModel(
            name="Trafficlight",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "direction",
                    models.CharField(
                        choices=[
                            ("LS", "Left straight"),
                            ("L", "Left"),
                            ("RS", "Right straight"),
                            ("R", "Right"),
                            ("A", "Any"),
                            ("S", "Straight"),
                        ],
                        max_length=100,
                    ),
                ),
                ("green_value", models.FloatField(default=0.5)),
                (
                    "crossroad",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="REST.crossroad",
                    ),
                ),
                (
                    "street",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="REST.street",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Webcam",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("active", models.BooleanField(default=False)),
                (
                    "crossroad",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="REST.crossroad",
                    ),
                ),
            ],
        ),
    ]
