# Generated by Django 2.1.7 on 2019-03-23 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190323_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visibletopost',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Author'),
        ),
    ]
