# Generated by Django 2.1.3 on 2018-11-18 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forumengine', '0007_category_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, default='default description', max_length=300),
        ),
    ]
