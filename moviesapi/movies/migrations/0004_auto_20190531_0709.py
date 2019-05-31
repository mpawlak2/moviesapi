# Generated by Django 2.2.1 on 2019-05-31 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movie_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='rated',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]