# Generated by Django 5.0.2 on 2024-03-22 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_customer_state_alter_movies_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='category',
            field=models.CharField(choices=[('T', 'Thriller'), ('E', 'Entertaintment'), ('SF', 'ScienceFiction'), ('R', 'Romance')], max_length=50),
        ),
    ]
