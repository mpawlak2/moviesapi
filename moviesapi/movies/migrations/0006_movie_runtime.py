# Generated by Django 2.2.1 on 2019-05-31 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_movie_released'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='runtime',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
    ]
