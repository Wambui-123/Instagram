# Generated by Django 4.0.5 on 2022-06-05 10:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_post_id_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.UUID('94a89aa0-8905-47c7-873b-cfacfb9591db'), editable=False, primary_key=True, serialize=False),
        ),
    ]