# Generated by Django 5.1.2 on 2024-10-22 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='shippingAddress2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
