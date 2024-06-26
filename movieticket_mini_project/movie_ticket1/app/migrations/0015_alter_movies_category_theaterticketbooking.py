# Generated by Django 5.0.2 on 2024-04-03 05:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_orderplaced_seat_selection_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='category',
            field=models.CharField(choices=[('T', 'Thriller'), ('E', 'Entertaintment'), ('SF', 'ScienceFiction'), ('R', 'Romance')], max_length=50),
        ),
        migrations.CreateModel(
            name='TheaterTicketBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.CharField(max_length=100)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.movies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
