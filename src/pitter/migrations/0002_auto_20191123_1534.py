# Generated by Django 2.2.7 on 2019-11-23 12:34

from django.db import migrations, models
import django.db.models.deletion
import pitter.models.base


class Migration(migrations.Migration):
    dependencies = [
        ('pitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pitt',
            fields=[
                ('id', models.CharField(default=pitter.models.base.default_uuid_id, editable=False, max_length=256,
                                        primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('speech_audio_file', models.FileField(upload_to='')),
                ('speech_transcription', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(default=pitter.models.base.default_uuid_id, editable=False, max_length=256,
                                        primary_key=True, serialize=False)),
                ('login',
                 models.CharField(error_messages={'unique': 'A user with this login already exists.'}, max_length=64,
                                  unique=True)),
                ('password', models.CharField(max_length=256)),
                ('profile_name', models.CharField(blank=True, max_length=64)),
                ('email', models.CharField(blank=True, max_length=128)),
                ('email_notifications_enabled', models.BooleanField(default=False)),
                ('joined_at', models.DateTimeField(auto_now=True)),
                ('last_action_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.AddField(
            model_name='pitt',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pitts',
                                    to='pitter.User'),
        ),
        migrations.AddField(
            model_name='follower',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets',
                                    to='pitter.User'),
        ),
        migrations.AddField(
            model_name='follower',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers',
                                    to='pitter.User'),
        ),
    ]
