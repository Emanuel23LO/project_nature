# Generated by Django 4.2.10 on 2024-02-28 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_alter_customer_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='name',
            new_name='full_name',
        ),
    ]
