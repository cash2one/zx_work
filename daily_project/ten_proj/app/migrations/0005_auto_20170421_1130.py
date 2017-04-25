# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-21 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170419_1656'),
    ]

    operations = [
        migrations.CreateModel(
            name='coTrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('op_unit_name', models.CharField(max_length=20, null=True, verbose_name='\u8fd0\u8425\u5355\u4f4d')),
                ('day_score', models.IntegerField(null=True, verbose_name='\u6bcf\u65e5\u79ef\u5206')),
                ('date', models.DateField(null=True, verbose_name='\u79ef\u5206\u65e5\u671f')),
            ],
            options={
                'db_table': 'index_co_trade',
                'verbose_name': '\u8fd0\u8425\u5355\u4f4d\u79ef\u5206\u8d8b\u52bf',
            },
        ),
        migrations.CreateModel(
            name='dpartTrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('op_unit_name', models.CharField(max_length=20, null=True, verbose_name='\u8fd0\u8425\u5355\u4f4d')),
                ('dpart', models.CharField(max_length=20, null=True, verbose_name='\u5927\u90e8')),
                ('day_score', models.IntegerField(null=True, verbose_name='\u6bcf\u65e5\u79ef\u5206')),
                ('date', models.DateField(null=True, verbose_name='\u79ef\u5206\u65e5\u671f')),
            ],
            options={
                'db_table': 'index_dp_trade',
                'verbose_name': '\u5927\u90e8\u79ef\u5206\u8d8b\u52bf\u56fe',
            },
        ),
        migrations.CreateModel(
            name='Intergral_rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spart', models.CharField(max_length=10)),
                ('sale_name', models.CharField(max_length=10, null=True)),
                ('month_rank', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'index_intergral_rank',
                'verbose_name': '\u4e2a\u4eba\u79ef\u5206\u6392\u540d',
            },
        ),
        migrations.CreateModel(
            name='personalScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('op_unit_name', models.CharField(max_length=20, verbose_name='\u8fd0\u8425\u5355\u4f4d')),
                ('dpart', models.CharField(max_length=10, verbose_name='\u5927\u90e8')),
                ('spart', models.CharField(max_length=10, verbose_name='\u5c0f\u90e8')),
                ('sale_name', models.CharField(max_length=20, verbose_name='\u9500\u552e\u4eba\u5458')),
                ('sale_num', models.CharField(max_length=20, verbose_name='\u4eba\u5458\u7f16\u53f7')),
                ('check_date', models.DateField(null=True, verbose_name='\u660e\u7ec6\u79ef\u5206\u65e5\u671f')),
                ('add_num', models.IntegerField(null=True, verbose_name='\u65b0\u589e\u7ebf\u7d22')),
                ('add_score', models.IntegerField(null=True, verbose_name='\u65b0\u589e\u79ef\u5206')),
                ('supple_tels', models.IntegerField(null=True, verbose_name='\u8865\u5145\u7535\u8bdd\u6570\u91cf')),
                ('supple_tels_score', models.IntegerField(null=True, verbose_name='\u8865\u5145\u7535\u8bdd\u79ef\u5206')),
                ('supple_num', models.IntegerField(null=True, verbose_name='\u6279\u91cf\u589e\u8865')),
                ('supple_score', models.IntegerField(null=True, verbose_name='\u589e\u8865\u79ef\u5206')),
                ('change_tels', models.IntegerField(null=True, verbose_name='\u4fee\u6b63\u7535\u8bdd')),
                ('change_tels_score', models.IntegerField(null=True, verbose_name='\u4fee\u6b63\u7535\u8bdd\u79ef\u5206')),
                ('chang_other', models.IntegerField(null=True, verbose_name='\u4fee\u6b63\u5176\u4ed6\u6570\u91cf')),
                ('chang_other_score', models.IntegerField(null=True, verbose_name='\u4fee\u6b63\u5176\u4ed6\u79ef\u5206')),
                ('abandon_tels', models.IntegerField(null=True, verbose_name='\u5e9f\u5f03\u7535\u8bdd\u6570\u91cf')),
                ('abandon_tels_score', models.IntegerField(null=True, verbose_name='\u5e9f\u5f03\u7535\u8bdd\u79ef\u5206')),
                ('change_trade', models.IntegerField(null=True, verbose_name='\u4fee\u6539\u884c\u4e1a\u6570\u91cf')),
                ('change_trade_score', models.IntegerField(null=True, verbose_name='\u4fee\u6539\u884c\u4e1a\u79ef\u5206')),
                ('pay_num', models.IntegerField(default=0, verbose_name='\u7ebf\u7d22\u8d21\u732e\u5230\u6b3e\u6570\u91cf')),
                ('pay_num_score', models.IntegerField(default=0, verbose_name='\u7ebf\u7d22\u8d21\u732e\u5230\u6b3e\u79ef\u5206')),
                ('day_score', models.IntegerField(default=0, verbose_name='\u5f53\u65e5\u79ef\u5206')),
                ('month_score', models.IntegerField(default=0, verbose_name='\u5f53\u6708\u79ef\u5206')),
                ('month_cost_score', models.IntegerField(null=True, verbose_name='\u5f53\u6708\u5151\u6362\u79ef\u5206')),
            ],
        ),
        migrations.DeleteModel(
            name='Integral_rank',
        ),
        migrations.AlterField(
            model_name='dpartdetail',
            name='completion_rate',
            field=models.FloatField(null=True, verbose_name='\u5b8c\u6210\u7387'),
        ),
        migrations.AlterField(
            model_name='dpartdetail',
            name='reach_rate',
            field=models.FloatField(null=True, verbose_name='\u8fbe\u6807\u7387'),
        ),
        migrations.AlterField(
            model_name='spartdetail',
            name='completion_rate',
            field=models.FloatField(null=True, verbose_name='\u5b8c\u6210\u7387'),
        ),
        migrations.AlterField(
            model_name='spartdetail',
            name='reach_rate',
            field=models.FloatField(null=True, verbose_name='\u8fbe\u6807\u7387'),
        ),
    ]