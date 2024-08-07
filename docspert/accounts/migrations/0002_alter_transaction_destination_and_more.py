# Generated by Django 5.0.7 on 2024-07-19 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="icoming_transactions",
                to="accounts.account",
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="outgoing_transactions",
                to="accounts.account",
            ),
        ),
    ]
