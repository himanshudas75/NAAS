# Generated by Django 4.2 on 2023-04-10 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0003_alter_user_managers_remove_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='username',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
