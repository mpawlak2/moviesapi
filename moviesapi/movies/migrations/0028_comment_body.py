# Generated by Django 2.2.1 on 2019-05-31 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0027_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='body',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
