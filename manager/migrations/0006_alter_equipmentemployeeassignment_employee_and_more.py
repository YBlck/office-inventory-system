# Generated by Django 5.1.6 on 2025-03-08 16:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0005_alter_equipment_assigned_to"),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipmentemployeeassignment",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="employees",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="equipmentemployeeassignment",
            name="equipment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assignments",
                to="manager.equipment",
            ),
        ),
    ]
