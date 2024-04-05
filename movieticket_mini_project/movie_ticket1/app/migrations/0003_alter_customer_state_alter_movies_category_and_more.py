# Generated by Django 5.0.2 on 2024-03-22 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_orderplaced_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(choices=[('Maharashtra', 'Maharashtra'), ('Goa', 'Goa')], max_length=50),
        ),
        migrations.AlterField(
            model_name='movies',
            name='category',
            field=models.CharField(choices=[('E', 'Entertaintment'), ('R', 'Romance'), ('SF', 'ScienceFiction'), ('T', 'Thriller')], max_length=50),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Cancel', 'Cancel'), ('Accepted', 'Accepted')], default='pending', max_length=50),
        ),
    ]
