# Generated by Django 2.1.5 on 2019-02-08 07:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('send_msg', '0006_auto_20190208_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Send date'),
        ),
    ]
