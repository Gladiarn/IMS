# Generated by Django 5.0.4 on 2024-06-23 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.CharField(default='admin', max_length=255),
        ),
    ]
