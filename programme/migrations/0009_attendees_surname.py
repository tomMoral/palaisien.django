# Generated by Django 2.2.5 on 2019-10-24 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0008_auto_20191018_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendees',
            name='surname',
            field=models.CharField(default='', max_length=256),
        ),
    ]
