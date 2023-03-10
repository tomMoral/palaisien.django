# Generated by Django 2.2.5 on 2019-10-18 13:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0005_auto_20191018_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='seminar',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='seminar time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seminar',
            name='date',
            field=models.DateField(verbose_name='seminar date'),
        ),
    ]
