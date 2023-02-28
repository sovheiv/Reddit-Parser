# Generated by Django 4.1.7 on 2023-02-28 20:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reddit_parser_api", "0002_alter_post_status_alter_post_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="comments_num",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="likes_num",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="parse_time",
            field=models.DateTimeField(null=True),
        ),
    ]