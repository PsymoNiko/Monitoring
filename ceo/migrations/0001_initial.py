# Generated by Django 4.1.7 on 2023-04-16 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("mentor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
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
                ("name", models.CharField(max_length=60)),
                ("start_at", models.DateField()),
                ("duration", models.PositiveSmallIntegerField(default=6)),
                ("class_time", models.TimeField()),
                (
                    "how_to_hold",
                    models.CharField(
                        choices=[("Online", "Online"), ("In person", "In person")],
                        max_length=15,
                    ),
                ),
                ("short_brief", models.CharField(max_length=70)),
                (
                    "mentor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mentor_of_course",
                        to="mentor.mentor",
                    ),
                ),
            ],
        ),
    ]
