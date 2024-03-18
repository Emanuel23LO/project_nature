# Generated by Django 4.2.10 on 2024-02-17 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookings', '0001_initial'),
        ('cabins', '0005_alter_cabin_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking_cabin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bookings.booking')),
                ('cabin', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cabins.cabin')),
            ],
        ),
    ]
