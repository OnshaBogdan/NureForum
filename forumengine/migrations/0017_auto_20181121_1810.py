# Generated by Django 2.1.3 on 2018-11-21 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forumengine', '0016_auto_20181121_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='author',
        ),
        migrations.RemoveField(
            model_name='message',
            name='topic',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='category',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
