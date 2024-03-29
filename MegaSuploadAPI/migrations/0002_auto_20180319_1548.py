# Generated by Django 2.0.2 on 2018-03-19 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MegaSuploadAPI', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='size',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='data_used',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='max_data_allowed',
            field=models.BigIntegerField(default=32212254720),
        ),
    ]
