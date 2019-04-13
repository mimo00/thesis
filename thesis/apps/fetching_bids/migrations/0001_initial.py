# Generated by Django 2.1.3 on 2019-04-06 13:30

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
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('mode', models.CharField(choices=[('hh', 'home-home'), ('hwh', 'home-work-home')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='ChargingLocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField()),
                ('departure_time', models.DateTimeField()),
                ('charge_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('expected_charge_percent', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charging_localizations', to='fetching_bids.Bid')),
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
            name='Localization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='localization',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fetching_bids.Node'),
        ),
        migrations.AddField(
            model_name='charginglocalization',
            name='localization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fetching_bids.Localization'),
        ),
        migrations.AddField(
            model_name='bid',
            name='electric_vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fetching_bids.ElectricVehicle'),
        ),
    ]
