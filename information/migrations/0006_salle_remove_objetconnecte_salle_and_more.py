# Generated by Django 5.1.7 on 2025-04-14 00:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("information", "0005_objetconnecte"),
    ]

    operations = [
        migrations.CreateModel(
            name="Salle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("normale", "Salle normale"),
                            ("avancee", "Salle avancée"),
                            ("premium", "Salle premium"),
                            ("commune", "Salle commune"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "niveau_min",
                    models.CharField(
                        choices=[
                            ("debutant", "Débutant"),
                            ("intermediaire", "Intermédiaire"),
                            ("avance", "Avancé"),
                            ("expert", "Expert"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="objetconnecte",
            name="salle",
        ),
        migrations.AddField(
            model_name="objetconnecte",
            name="salle_associee",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="information.salle",
            ),
            preserve_default=False,
        ),
    ]
