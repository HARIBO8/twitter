# Generated by Django 4.2.20 on 2025-06-18 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_tweet_parent_alter_tweet_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='original',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='retweets', to='core.tweet'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
