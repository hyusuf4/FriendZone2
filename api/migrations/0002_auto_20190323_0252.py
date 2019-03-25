# Generated by Django 2.1.7 on 2019-03-23 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='visibletopost',
            name='author_url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='postid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='api.Post'),
        ),
    ]