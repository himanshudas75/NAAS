# Generated by Django 4.2 on 2023-04-11 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0009_user_deliveries_delete_deliveries'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='salary',
            field=models.FloatField(null=True),
        ),
    ]
