# Generated by Django 5.1.1 on 2024-09-23 18:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_remove_course_enrolled_users_course_number_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='smt',
            new_name='course_id',
        ),
        migrations.RemoveField(
            model_name='course',
            name='number',
        ),
        migrations.AddField(
            model_name='course',
            name='enrolled_users',
            field=models.ManyToManyField(blank=True, related_name='courses', to=settings.AUTH_USER_MODEL),
        ),
    ]