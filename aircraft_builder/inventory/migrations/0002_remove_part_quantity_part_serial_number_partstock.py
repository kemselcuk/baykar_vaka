# Generated by Django 4.2.3 on 2024-12-21 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='quantity',
        ),
        migrations.AddField(
            model_name='part',
            name='serial_number',
            field=models.CharField(default=1, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='PartStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_type', models.CharField(choices=[('KANAT', 'Kanat'), ('GOVDE', 'Gövde'), ('KUYRUK', 'Kuyruk'), ('AVIYONIK', 'Aviyonik')], max_length=20)),
                ('aircraft_type', models.CharField(choices=[('TB2', 'TB2'), ('TB3', 'TB3'), ('AKINCI', 'AKINCI'), ('KIZILELMA', 'KIZILELMA')], max_length=20)),
                ('quantity', models.PositiveIntegerField(default=0)),
            ],
            options={
                'unique_together': {('part_type', 'aircraft_type')},
            },
        ),
    ]