# Generated by Django 2.1.3 on 2019-05-08 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregatorDecision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision_date', models.DateField(unique=True)),
                ('receive_date', models.DateTimeField()),
                ('energy_coverage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('hour_coverage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('energy_loss', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='PointScheduleDecision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('coverage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('decision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='point_schedule_decisions', to='decisions.AggregatorDecision')),
                ('point_schedule', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='schedules.PointSchedule')),
            ],
        ),
    ]
