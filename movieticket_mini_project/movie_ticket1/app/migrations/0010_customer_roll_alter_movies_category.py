# Generated by Django 5.0.3 on 2024-03-30 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_movies_address_movies_show_time_movies_theater_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='roll',
            field=models.CharField(choices=[('user', 'User'), ('theater', 'Theater')], default='user', max_length=10),
        ),
        migrations.AlterField(
            model_name='movies',
            name='category',
            field=models.CharField(choices=[('SF', 'ScienceFiction'), ('R', 'Romance'), ('T', 'Thriller'), ('E', 'Entertaintment')], max_length=50),
        ),
    ]
