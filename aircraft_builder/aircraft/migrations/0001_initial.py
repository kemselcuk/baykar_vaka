# Generated by Django 4.2.3 on 2024-12-19 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProducedAircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aircraft_type', models.CharField(choices=[('TB2', 'TB2'), ('TB3', 'TB3'), ('AKINCI', 'AKINCI'), ('KIZILELMA', 'KIZILELMA')], max_length=20)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
