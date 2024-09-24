# Generated by Django 5.1.1 on 2024-09-24 12:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('semester', models.PositiveIntegerField(default=0)),
                ('year', models.PositiveIntegerField(default=0)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('is_open', models.BooleanField(default=True)),
                ('enrolled_users', models.ManyToManyField(blank=True, related_name='courses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
