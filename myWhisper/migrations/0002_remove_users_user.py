# Generated by Django 3.2.25 on 2024-06-27 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myWhisper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='user',
        ),
    ]
