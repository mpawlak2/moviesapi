# Generated by Django 2.2.1 on 2019-05-31 05:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20190531_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='released',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
