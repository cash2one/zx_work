# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-25 00:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170421_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='monthGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('op_unit_name', models.CharField(max_length=20, null=True, verbose_name='\u8fd0\u8425\u5355\u4f4d')),
                ('goal_date', models.DateField(null=True, verbose_name='\u79ef\u5206\u65e5\u671f')),
                ('avg_score_goal', models.IntegerField(null=True, verbose_name='\u4eba\u6708\u76ee\u6807\u79ef\u5206')),
            ],
            options={
                'db_table': 'index_month_goal',
                'verbose_name': '\u6708\u5ea6\u4eba\u5747\u76ee\u6807\u79ef\u5206',
            },
        ),
        migrations.AlterModelOptions(
            name='daily',
            options={'verbose_name': '\u6bcf\u65e5\u79ef\u5206\u660e\u7ec6(\u540c\u6b65)'},
        ),
    ]
