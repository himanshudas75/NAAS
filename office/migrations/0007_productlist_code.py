# Generated by Django 4.2 on 2023-04-10 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0006_subscriptionlist_unique_customer_product_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='productlist',
            name='code',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
