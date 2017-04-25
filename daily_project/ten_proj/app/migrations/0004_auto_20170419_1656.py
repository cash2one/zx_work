# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-19 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170419_0833'),
    ]

    operations = [
        migrations.CreateModel(
            name='DpartDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dpart', models.CharField(max_length=10, verbose_name='\u5927\u90e8')),
                ('crews', models.IntegerField(null=True, verbose_name='\u4eba\u6570')),
                ('add_num', models.IntegerField(null=True, verbose_name='\u65b0\u589e\u7ebf\u7d22')),
                ('supple_tels', models.IntegerField(null=True, verbose_name='\u8865\u5145\u7535\u8bdd\u6570\u91cf')),
                ('supple_num', models.IntegerField(null=True, verbose_name='\u6279\u91cf\u589e\u8865')),
                ('change_tels', models.IntegerField(null=True, verbose_name='\u4fee\u6b63\u7535\u8bdd')),
                ('chang_other', models.IntegerField(null=True, verbose_name='\u4fee\u6b63\u5176\u4ed6\u6570\u91cf')),
                ('abandon_tels', models.IntegerField(null=True, verbose_name='\u5e9f\u5f03\u7535\u8bdd\u6570\u91cf')),
                ('change_trade', models.IntegerField(null=True, verbose_name='\u4fee\u6539\u884c\u4e1a\u6570\u91cf')),
                ('pay_num', models.IntegerField(default=0, verbose_name='\u7ebf\u7d22\u8d21\u732e\u5230\u6b3e')),
                ('score_sum', models.IntegerField(default=0, verbose_name='\u603b\u79ef\u5206')),
                ('month_goal', models.IntegerField(default=0, verbose_name='\u6708\u5ea6\u76ee\u6807\u79ef\u5206')),
                ('completion_rate', models.IntegerField(null=True, verbose_name='\u5b8c\u6210\u7387')),
                ('reach_rate', models.IntegerField(null=True, verbose_name='\u8fbe\u6807\u7387')),
                ('vaild_rank', models.IntegerField(null=True, verbose_name='\u53ef\u7528\u79ef\u5206')),
            ],
            options={
                'db_table': 'index_big_depart_data',
                'verbose_name': '\u5927\u90e8\u79ef\u5206\u660e\u7ec6\u8868',
            },
        ),
        migrations.CreateModel(
            name='SpartDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spart', models.CharField(max_length=10, verbose_name='\u5c0f\u90e8')),
                ('crews', models.IntegerField(null=True, verbose_name='\u4eba\u6570')),
                ('add_num', models.IntegerField(null=True, verbose_name='\u65b0\u589e\u7ebf\u7d22')),
                ('supple_tels', models.IntegerField(null=True, verbose_name='\u8865\u5145\u7535\u8bdd\u6570\u91cf')),
                ('supple_num', models.IntegerField(null=True, verbose_name='\u6279\u91cf\u589e\u8865')),
                ('change_tels', models.IntegerField(null=True, verbose_name='\u4fee\u6b63\u7535\u8bdd')),
                ('chang_other', models.IntegerField(null=True, verbose_name='\u4fee\u6b63\u5176\u4ed6\u6570\u91cf')),
                ('abandon_tels', models.IntegerField(null=True, verbose_name='\u5e9f\u5f03\u7535\u8bdd\u6570\u91cf')),
                ('change_trade', models.IntegerField(null=True, verbose_name='\u4fee\u6539\u884c\u4e1a\u6570\u91cf')),
                ('pay_num', models.IntegerField(default=0, verbose_name='\u7ebf\u7d22\u8d21\u732e\u5230\u6b3e')),
                ('score_sum', models.IntegerField(default=0, verbose_name='\u603b\u79ef\u5206')),
                ('month_goal', models.IntegerField(default=0, verbose_name='\u6708\u5ea6\u76ee\u6807\u79ef\u5206')),
                ('completion_rate', models.IntegerField(null=True, verbose_name='\u5b8c\u6210\u7387')),
                ('reach_rate', models.IntegerField(null=True, verbose_name='\u8fbe\u6807\u7387')),
                ('vaild_rank', models.IntegerField(null=True, verbose_name='\u53ef\u7528\u79ef\u5206')),
            ],
            options={
                'db_table': 'index_small_depart_data',
                'verbose_name': '\u5c0f\u90e8\u79ef\u5206\u660e\u7ec6\u8868',
            },
        ),
        migrations.DeleteModel(
            name='polls',
        ),
        migrations.AlterModelOptions(
            name='all',
            options={'verbose_name': '\u7d2f\u8ba1\u79ef\u5206\u6c47\u603b\u8868\uff08\u540c\u6b65\uff09'},
        ),
        migrations.AlterModelOptions(
            name='big_depart_data',
            options={'verbose_name': '\u5927\u90e8\u79ef\u5206'},
        ),
        migrations.AlterModelOptions(
            name='change',
            options={'verbose_name': '\u53d8\u66f4\u5355\u660e\u7ec6'},
        ),
        migrations.AlterModelOptions(
            name='daily',
            options={'verbose_name': '\u6bcf\u65e5\u79ef\u5206\u660e\u7ec6'},
        ),
        migrations.AlterModelOptions(
            name='integral_rank',
            options={'verbose_name': '\u4e2a\u4eba\u79ef\u5206\u6392\u540d'},
        ),
        migrations.AlterModelOptions(
            name='new',
            options={'verbose_name': '\u65b0\u589e\u660e\u7ec6'},
        ),
        migrations.AlterModelTable(
            name='all',
            table='index_all',
        ),
        migrations.AlterModelTable(
            name='big_depart_data',
            table='big_depart_data',
        ),
        migrations.AlterModelTable(
            name='change',
            table='index_change',
        ),
        migrations.AlterModelTable(
            name='daily',
            table='index_daily',
        ),
        migrations.AlterModelTable(
            name='integral_rank',
            table='index_integral_rank',
        ),
        migrations.AlterModelTable(
            name='new',
            table='index_new',
        ),
    ]