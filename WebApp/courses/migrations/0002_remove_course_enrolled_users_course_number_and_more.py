# Generated by Django 5.1.1 on 2024-09-23 17:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='enrolled_users',
        ),
        migrations.AddField(
            model_name='course',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='semester',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='smt',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='course',
            name='capacity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]