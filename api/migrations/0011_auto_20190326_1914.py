# Generated by Django 2.1.7 on 2019-03-26 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20190326_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='author1_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='friends',
            name='author2_url',
            field=models.URLField(null=True),
        ),
    ]
