# Generated by Django 3.1.3 on 2020-11-13 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('mail', models.EmailField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_id', models.IntegerField(unique=True)),
                ('destination_address', models.CharField(max_length=200)),
                ('destination_phone', models.IntegerField(blank=True, default=0)),
                ('destination_name', models.CharField(blank=True, max_length=200)),
                ('weigth', models.FloatField(default=1)),
                ('heigth', models.FloatField(blank=True, null=True)),
                ('size', models.CharField(default='S', max_length=2)),
                ('client', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='package_system.client')),
            ],
        ),
        migrations.CreateModel(
            name='SpreadSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sheet_id', models.IntegerField(unique=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SheetItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('pos', models.IntegerField()),
                ('status', models.IntegerField(choices=[(1, 'Complete'), (2, 'Lost'), (3, 'Damaged'), (4, 'Incomplete')], default=1)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='package_system.package')),
                ('spreadsheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='package_system.spreadsheet')),
            ],
        ),
    ]
