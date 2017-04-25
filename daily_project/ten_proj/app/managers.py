#coding:utf-8
from django.db import models
from datetime import datetime
import calendar

# 根据累计积分提取

now_day = datetime.now()
month_firstday = datetime.strptime(datetime.strftime(now_day,'%Y-%m')+'-01','%Y-%m-%d')
lastday = str(calendar.monthrange(now_day.year,now_day.month)[1])
month_lastday = datetime.strptime(datetime.strftime(now_day,'%Y-%m')+'-'+lastday,'%Y-%m-%d')
class allManager(models.Manager):
    #运营单位趋势图的表内容
    co_trade_exist = coTrade.objects.one()  # 运营单位趋势表是否有内容
    dp_trade_exist = dpartTrade.objects.one() # 大部趋势表是否有内容
    dp_detail_exist = dpartTrade.objects.one() # 大部积分明细表是否有内容
    sp_detail_exist = spartTrade.objects.one() # 小部积分明细是否有内容

    def get_co_trade(self):
        if not co_trade_exist:
            """运营单位趋势图无数据则取累计分中所有数据的总积分进行分组"""
            query_day_score = self.get_queryset().values('op_unit_name','deadline_date')\
                .annotate(today_score = sum('today_score')).values('op_unit_name',\
                'deadline_date','today_score')
        else:
            """选取部分天数的积分作为更新到运营单位趋势表的凭据"""
            query_day_score = self.get_queryset().filter(deadline_date__gte = month_firstday,\
                deadline_date__lte = month_lastday).values('op_unit_name','deadline_date')\
                .annotate(today_score = sum('today_score')).values('op_unit_name',\
                'deadline_date','today_score')
        return query_day_score

    def get_dp_trade(self,unit_name):
        if not dp_trade_exist:
            """大部趋势表无数据则取累计积分中按大部分组后的所有数据"""
            query_day_score = self.get_queryset().filter(op_unit_name = unit_name).values('dpart',\
                'deadline_date').annotate(today_score = sum('today_score')).values(\
                'dpart','today_score','deadline_date')

        else:
            """选取部分天数的积分作为更新用"""
            query_day_score = self.get_queryset().filter(op_unit_name = unit_name,\
                deadline_date__gte = month_firstday,deadline_date__lte = datetime.now()).values(\
                'dpart','deadline_date').annotate(today_score = sum('today_score')).values(\
                'dpart','today_score','deadline_date')
        return query_day_score

    #大部达标率&月度总积分
    def get_dp_reach_all(self): ####如何将历史数据按照月份统计内容
        """大部积分明细 de 达标率，月度总积分，完成率，可用积分的和计算"""
        if not dp_detail_exist:
            query_all = self.get_queryset().all()
            all_list = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_dp_reach = self.get_queryset().filter(today_score_gte = 1000,deadline_date = i.deadline_date\
                    ).values('dpart').annotate(today_reach = sum('today_score')).values('dpart','deadline_date',\
                    'today_reach')
                query_all_reach = self.get_queryset().filter(deadline_date = i.deadline_date,\
                    ).values('dpart').annotate(today_all_score = sum('this_month_score')).values(\
                    'dpart','deadline_date','today_all_score')
                query = {'dpart':query_all_reach.dpart,'deadline_date':query_all_reach.deadline_date,\
                    'reach_rank':round(float(query_dp_reach.today_reach/query_all_reach.today_all_score)*100,2),\
                    'this_month_score':query_all_reach.today_all_score}
                all_list.append(query)
        else:
            query_all = self.get_queryset().filter(deadline_date__lte = datetime.now(),deadline_date__gte = month_first)
            all_list = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_dp_reach = self.get_queryset().filter(today_score_gte = 1000,deadline_date = i.deadline_date\
                    ).values('dpart').annotate(today_reach = sum('today_score')).values('dpart','deadline_date',\
                    'today_reach')
                query_all_reach = self.get_queryset().filter(deadline_date = i.deadline_date,\
                    ).values('dpart').annotate(today_all_score = sum('this_month_score')).values(\
                    'dpart','deadline_date','today_all_score')
                query = {'dpart':query_all_reach.dpart,'deadline_date':query_all_reach.deadline_date,\
                    'reach_rank':round(float(query_dp_reach.today_reach/query_all_reach.today_all_score)*100,2),\
                    'this_month_score':query_all_reach.today_all_score}
                all_list.append(query)
        return all_list

    # 大部每日可用积分
    def  get_dp_vaild(self):
        if not dp_detail_exist:
            query_all = self.get_queryset().all()
            all_list = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_dp_vaild = self.get_queryset().filter(deadline_date = i.deadline_date\
                    ).values('dpart').annotate(vaild_rank = sum('his_all_score')-sum('his_cost_score')\
                    ).values('dpart','deadline_date','vaild_rank')
                all_list.append(query_dp_vaild)
        else:
            query_all = self.get_queryset().filter(deadline_date__lte = datetime.now(),deadline_date__gte = month_first)
            all_list = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_dp_vaild = self.get_queryset().filter(deadline_date = i.deadline_date\
                    ).values('dpart').annotate(vaild_rank = sum('his_all_score')-sum('his_cost_score')\
                    ).values('dpart','deadline_date','vaild_rank')
                all_list.append(query_dp_vaild)
        return all_list

    # 小部达标率&每日的月度总积分
    def get_sp_reach_all(self):
        """小部积分明细之达标率，月度总积分，完成率，可用积分的和计算"""
        if not sp_detail_exist:
            query_all = self.get_queryset().all()
            all_list = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_sp_reach = self.get_queryset().filter(today_score_gte = 1000,deadline_date = i.deadline_date\
                    ).values('spart').annotate(today_reach = sum('today_score')).values('spart','deadline_date',\
                    'today_reach')
                query_all_reach = self.get_queryset().filter(deadline_date = i.deadline_date,\
                    ).values('spart').annotate(today_all_score = sum('this_month_score')).values(\
                    'spart','deadline_date','today_all_score')
                query = {'spart':query_all_reach.spart,'deadline_date':query_all_reach.deadline_date,\
                    'reach_rank':round(float(query_sp_reach.today_reach/query_all_reach.today_all_score)*100,2),\
                    'this_month_score':query_all_reach.today_all_score}
                all_list.append(query)
        else:
            query_all = self.get_queryset().filter(deadline_date__lte = datetime.now(),deadline_date__gte = month_first)
            all_list = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_sp_reach = self.get_queryset().filter(today_score_gte = 1000,deadline_date = i.deadline_date\
                    ).values('spart').annotate(today_reach = sum('today_score')).values('spart','deadline_date',\
                    'today_reach')
                query_all_reach = self.get_queryset().filter(deadline_date = i.deadline_date,\
                    ).values('spart').annotate(today_all_score = sum('this_month_score')).values(\
                    'spart','deadline_date','today_all_score')
                query = {'spart':query_all_reach.spart,'deadline_date':query_all_reach.deadline_date,\
                    'reach_rank':round(float(query_sp_reach.today_reach/query_all_reach.today_all_score)*100,2),\
                    'this_month_score':query_all_reach.today_all_score}
                all_list.append(query)
        return all_list

    def  get_sp_vaild(self):
        if not sp_detail_exist:
            query_all = self.get_queryset().all()
            all_list = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_sp_vaild = self.get_queryset().filter(deadline_date = i.deadline_date\
                    ).values('spart').annotate(vaild_rank = sum('his_all_score')-sum('his_cost_score')\
                    ).values('spart','deadline_date','vaild_rank')
                all_list.append(query_sp_vaild)
        else:
            query_all = self.get_queryset().filter(deadline_date__lte = datetime.now(),deadline_date__gte = month_first)
            all_list = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_sp_vaild = self.get_queryset().filter(deadline_date = i.deadline_date\
                    ).values('spart').annotate(vaild_rank = sum('his_all_score')-sum('his_cost_score')\
                    ).values('spart','deadline_date','vaild_rank')
                all_list.append(query_sp_vaild)
        return all_list
