# Generated by Django 3.2.5 on 2021-09-25 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0002_atmdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atmdetails',
            name='openingHours',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
