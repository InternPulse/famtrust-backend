# Generated by Django 5.0.7 on 2024-08-01 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("family_memberships", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="familymembership",
            options={"ordering": ("-joined_at",)},
        ),
    ]
