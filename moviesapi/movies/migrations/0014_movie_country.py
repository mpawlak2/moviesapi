# Generated by Django 2.2.1 on 2019-05-31 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_movie_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]