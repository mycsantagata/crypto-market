# Generated by Django 2.2.28 on 2022-09-02 07:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "_id",
                    djongo.models.fields.ObjectIdField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("btc", models.IntegerField(default=1, null=True)),
                ("dollar", models.IntegerField(default=10000, null=True)),
                ("earning", models.FloatField(default=0)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "_id",
                    djongo.models.fields.ObjectIdField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "datetime",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2022, 9, 2, 7, 33, 49, 379435, tzinfo=utc
                        )
                    ),
                ),
                (
                    "type",
                    models.IntegerField(choices=[(1, "BUY"), (2, "SELL")], null=True),
                ),
                ("price", models.FloatField(null=True)),
                ("quantity", models.FloatField(null=True)),
                ("fill", models.FloatField(default=0, null=True)),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "Active"), (2, "Executed")], null=True
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.Profile"
                    ),
                ),
            ],
        ),
    ]
