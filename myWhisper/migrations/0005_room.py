# Generated by Django 5.0.6 on 2024-07-03 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myWhisper', '0004_alter_message_receiver_alter_message_sender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('messages', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mesages', to='myWhisper.message')),
            ],
        ),
    ]
