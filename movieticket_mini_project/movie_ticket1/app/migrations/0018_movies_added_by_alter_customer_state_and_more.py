# Generated by Django 5.0.2 on 2024-04-04 06:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_theaterticketbooking_seat1_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='added_movies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(choices=[('Maharashtra', 'Maharashtra'), ('Goa', 'Goa')], max_length=50),
        ),
        migrations.AlterField(
            model_name='movies',
            name='category',
            field=models.CharField(choices=[('E', 'Entertaintment'), ('SF', 'ScienceFiction'), ('R', 'Romance'), ('T', 'Thriller')], max_length=50),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Cancel', 'Cancel'), ('Booked', 'Booked')], default='Pending', max_length=50),
        ),
    ]
