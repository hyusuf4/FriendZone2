# Generated by Django 2.1.7 on 2019-03-26 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20190326_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friends',
            name='author1_url',
        ),
        migrations.RemoveField(
            model_name='friends',
            name='author2_url',
        ),
    ]
