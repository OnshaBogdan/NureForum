# Generated by Django 2.1.3 on 2018-11-21 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forumengine', '0012_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='slug',
            new_name='cat_slug',
        ),
    ]
