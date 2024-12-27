# Generated by Django 5.1.4 on 2024-12-27 00:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=20)),
                ('court', models.CharField(max_length=10)),
                ('action', models.CharField(max_length=10)),
                ('user', models.CharField(max_length=50)),
                ('user_role', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modification_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modification_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modification_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCourt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('nature', models.IntegerField()),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modification_time', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modification_time', models.DateTimeField(auto_now=True)),
                ('item_court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.itemcourt')),
            ],
        ),
        migrations.CreateModel(
            name='ItemOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.DecimalField(decimal_places=2, max_digits=10)),
                ('flag', models.IntegerField()),
                ('date', models.DateField()),
                ('status', models.BooleanField()),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('modification_time', models.DateTimeField(auto_now=True)),
                ('item_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.itemtime')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.venue'),
        ),
    ]
