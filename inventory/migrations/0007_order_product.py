# Generated by Django 5.0.4 on 2024-06-26 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_remove_order_status_alter_order_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
