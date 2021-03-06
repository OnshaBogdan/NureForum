# Generated by Django 2.1.3 on 2018-11-18 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('forumengine', '0006_auto_20181118_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='test', max_length=80)),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('topic_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(default='unnamed', max_length=80)),
                ('date_of_pub', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forumengine.Category')),
            ],
        ),
    ]
