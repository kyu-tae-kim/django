# Generated by Django 5.1.2 on 2024-10-30 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_alter_answer_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='modify_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='modify_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]