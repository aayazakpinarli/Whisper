# Generated by Django 5.0.6 on 2024-07-04 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myWhisper', '0006_thread_chatmessage_delete_room'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
