# Generated by Django 4.2 on 2023-04-11 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0012_customer_due_days_customer_pause'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='amount_payable',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='productlist',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='deliveries',
            field=models.FloatField(default=0),
        ),
    ]