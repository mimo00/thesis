# Generated by Django 2.1.3 on 2019-05-18 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargingPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ElectricVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_battery_capacity', models.IntegerField()),
                ('min_battery_capacity', models.IntegerField()),
                ('max_charging_power', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PointSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField()),
                ('departure_time', models.DateTimeField()),
                ('point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.ChargingPoint')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('mode', models.CharField(choices=[('hh', 'home-home'), ('hwh', 'home-work-home')], max_length=3)),
                ('charge_percent', models.IntegerField()),
                ('trip_percent', models.IntegerField()),
                ('electric_vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.ElectricVehicle')),
            ],
        ),
        migrations.AddField(
            model_name='pointschedule',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='point_schedules', to='schedules.Schedule'),
        ),
        migrations.AddField(
            model_name='chargingpoint',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.Node'),
        ),
    ]
