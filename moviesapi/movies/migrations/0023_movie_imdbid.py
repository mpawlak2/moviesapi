# Generated by Django 2.2.1 on 2019-05-31 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0022_movie_imdbvotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdbid',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
