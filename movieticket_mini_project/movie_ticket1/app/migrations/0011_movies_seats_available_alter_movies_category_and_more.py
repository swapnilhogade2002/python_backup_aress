# Generated by Django 5.0.3 on 2024-03-30 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_customer_roll_alter_movies_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='seats_available',
            field=models.IntegerField(default=100),
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
