# Generated by Django 2.1.7 on 2019-03-12 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190312_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publicationDate',
            field=models.DateField(),
        ),
    ]