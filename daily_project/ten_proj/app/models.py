#coding:utf-8
from __future__ import unicode_literals
from django.db import models
#from managers import *
# Create your models here.
# 与eccrc同步的累计积分 和 每日积分明细
# 运营单位趋势积分表

from datetime import datetime
import calendar

# 根据累计积分提取

now_day = datetime.now().date()
month_firstday = datetime.strptime(datetime.strftime(now_day,'%Y-%m')+'-01','%Y-%m-%d')
lastday = str(calendar.monthrange(now_day.year,now_day.month)[1])
month_lastday = datetime.strptime(datetime.strftime(now_day,'%Y-%m')+'-'+lastday,'%Y-%m-%d')
class allManager(models.Manager):
    #运营单位趋势图的表内容
    #co_trade_exist = coTrade.objects.one()  # 运营单位趋势表是否有内容
    #dp_trade_exist = dpartTrade.objects.one() # 大部趋势表是否有内容
    #dp_detail_exist = dpartTrade.objects.one() # 大部积分明细表是否有内容
    #sp_detail_exist = spartTrade.objects.one() # 小部积分明细是否有内容

    def get_co_trade(self,is_exist):
        #if not co_trade_exist:
        if not is_exist:
            """运营单位趋势图无数据则取累计分中所有数据的总积分进行分组"""
            query_day_score = self.get_queryset().values('op_unit_name','deadline_date')\
                .annotate(today_score = sum('today_score')).values('op_unit_name',\
                'deadline_date','today_score').order_by("deadlint_date")
        else:
            """选取部分天数的积分作为更新到运营单位趋势表的凭据"""
            query_day_score = self.get_queryset().filter(deadline_date__gte = month_firstday,\
                deadline_date__lte = month_lastday).values('op_unit_name','deadline_date')\
                .annotate(today_score = sum('today_score')).values('op_unit_name',\
                'deadline_date','today_score').order_by("deadlint_date")
        return query_day_score

    def get_dp_trade(self,is_exist,unit_name):
        #if not dp_trade_exist:
        if not is_exist:
            """大部趋势表无数据则取累计积分中按大部分组后的所有数据"""
            query_day_score = self.get_queryset().filter(op_unit_name = unit_name).values('db',\
                'deadline_date').annotate(today_score = sum('today_score')).values(\
                'db','today_score','deadline_date').order_by("deadlint_date")

        else:
            """选取部分天数的积分作为更新用"""
            query_day_score = self.get_queryset().filter(op_unit_name = unit_name,\
                deadline_date__gte = month_firstday,deadline_date__lte = datetime.now()).values(\
                'db','deadline_date').annotate(today_score = sum('today_score')).values(\
                'db','today_score','deadline_date').order_by("deadlint_date")
        return query_day_score


    #大部人数&月度总积分
    def get_dp_reach_all(self,is_exist,unit_name): ####如何将历史数据按照月份统计内容
        """大部积分明细 de 人数，月度总积分"""
        #if not dp_detail_exist:
        if not is_exist:
            query_all = self.get_queryset().all()
            query = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_dp = self.get_queryset().filter(deadline_date = i.deadline_date\
                    ).values('db',unit_name).annotate(man_num = sum('sale_name'),\
                    this_month_score =sum('this_month_score')).values('op_unit_name','db','man_num',\
                    'deadline_date','this_month_score')
                query.append(query_dp)
        else:
            query = self.get_queryset().filter(deadline_date = now_day).values('depart',unit_name).annotate(man_num=count('sale_name'),\
                this_month_score = sum('this_month_score')).values('op_unit_name','db','man_num','this_month_score')
        return query

    # 大部每日可用积分
    def  get_dp_vaild(self,is_exist,unit_name,db):
        #if not dp_detail_exist:
        if not is_exist:
            query_all = self.get_queryset().all()
            query = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_dp_vaild = self.get_queryset().filter(deadline_date = i.deadline_date\
                    ).values('db').annotate(vaild_rank = sum('his_all_score')-sum('his_cost_score')\
                    ).values('db','deadline_date','vaild_rank')
                query.append(query_dp_vaild)
        else:
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_dp_vaild = self.get_queryset().filter(deadline_date = now_day,op_unit_name = unit_name,db = db\
                    ).values('db').annotate(vaild_rank = sum('his_all_score')-sum('his_cost_score')\
                    ).values('db','deadline_date','vaild_rank')
                query.append(query_dp_vaild)
        return query

    # 小部人数，月度总积分
    def get_sp_reach_all(self,is_exist,unit_name):
        """小部积分明细之人数，月度总积分"""
        #if not sp_detail_exist:
        if not is_exist:
            query_all = self.get_queryset().all()
            query = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_sp = self.get_queryset().filter(deadline_date = i.deadline_date,op_unit_name = unit_name).values('xb','db').annotate(man = count('sale_name'),\
                    today_reach_score = sum('this_month_score')).values('xb','deadline_date',\
                    'sales_name','today_all_score')
                query.append(query)
        else:
            query = self.get_queryset().filter(deadline_date = now_day,op_unit_name = unit_name).values('xb','db',\
                'op_unit_name').annotate(man_num = count('sale_name'),this_month_score = sum('this_month_score')).values('xb',\
                'db','op_unit_name','man_num','this_month_score')
        return query

    def  get_sp_vaild(self,is_exist,unit_name,xb):
        #if not sp_detail_exist:
        if not is_exist:
            query_all = self.get_queryset().all()
            query = []
            for i in query_all:# oneday sum(today>1000)/oneday sum(this_month_score)
                query_sp_vaild = self.get_queryset().filter(deadline_date = i.deadline_date,op_unit_name = unit_name\
                    ).values('xb').annotate(vaild_rank = sum('his_all_score')-sum('his_cost_score')\
                    ).values('xb','deadline_date','vaild_rank')
                query.append(query_sp_vaild)
        else:
                query = self.get_queryset().filter(deadline_date = now_day,op_unit_name = unit_name,xb = xb).values('xb'\
                    ).annotate(vaild_rank = sum('his_all_score')-sum('his_cost_score')\
                    ).values('xb','deadline_date','vaild_rank')

        return query

class dailyManager(object):
    #大部明细积分
    def get_dp_detail(self,is_exist,unit_name):
        if not is_exist:
            query_detail = self.get_queryset().filter(op_unit_name = unit_name).values('db',\
                'check_date').annotate(newadd_num = sum('newadd_num'),newadd_score = sum('newadd_score'),\
                pay_num = sum('pay_num'), pay_score = sum('pay_score'), supple_num = sum('supple_num'),\
                supple_score = sum('supple_score'),supple_ph_num = sum('supple_ph_num'), \
                supple_ph_score = sum('supple_ph_score'), chang_ph_num = sum('chang_ph_num'),\
                chang_ph_score = sum('chang_ph_score'), chang_other_num = sum('chang_other_num'),\
                chang_other_score = sum('chang_other_score'), abandon_ph_num = sum('abandon_ph_num'),\
                abandon_ph_score = sum('abandon_ph_score'), chang_trade_num = sum('chang_trade_num'),\
                chang_trade_score = sum('chang_trade_score')).values('newadd_num','newadd_score',\
                'pay_num', 'pay_score','supple_num','supple_score','supple_ph_num','supple_ph_score',\
                'chang_ph_num','chang_ph_score', 'chang_other_num','chang_other_score', 'abandon_ph_num',\
                'abandon_ph_score', 'chang_trade_num','chang_trade_score','db','check_date')
        else:
            query_detail = self.get_queryset().filter(op_unit_name = unit_name,check_date__gte = now_day\
                ).values('db','check_date').annotate(newadd_num = sum('newadd_num'),\
                newadd_score = sum('newadd_score'),pay_num = sum('pay_num'), pay_score = sum('pay_score'), \
                supple_num = sum('supple_num'),supple_score = sum('supple_score'),supple_ph_num = sum('supple_ph_num'), \
                supple_ph_score = sum('supple_ph_score'), chang_ph_num = sum('chang_ph_num'),\
                chang_ph_score = sum('chang_ph_score'), chang_other_num = sum('chang_other_num'),\
                chang_other_score = sum('chang_other_score'), abandon_ph_num = sum('abandon_ph_num'),\
                abandon_ph_score = sum('abandon_ph_score'), chang_trade_num = sum('chang_trade_num'),\
                chang_trade_score = sum('chang_trade_score')).values('newadd_num','newadd_score',\
                'pay_num', 'pay_score','supple_num','supple_score','supple_ph_num','supple_ph_score',\
                'chang_ph_num','chang_ph_score', 'chang_other_num','chang_other_score', 'abandon_ph_num',\
                'abandon_ph_score', 'chang_trade_num','chang_trade_score','db','check_date')
        return query_detail

    #小部明细积分
    def get_sp_detail(self,is_exist,unit_name):
        if not is_exist:
            query_detail = self.get_queryset().filter(op_unit_name = unit_name).values('xb',\
                'check_date').annotate(newadd_num = sum('newadd_num'),newadd_score = sum('newadd_score'),\
                pay_num = sum('pay_num'), pay_score = sum('pay_score'), supple_num = sum('supple_num'),\
                supple_score = sum('supple_score'),supple_ph_num = sum('supple_ph_num'), \
                supple_ph_score = sum('supple_ph_score'), chang_ph_num = sum('chang_ph_num'),\
                chang_ph_score = sum('chang_ph_score'), chang_other_num = sum('chang_other_num'),\
                chang_other_score = sum('chang_other_score'), abandon_ph_num = sum('abandon_ph_num'),\
                abandon_ph_score = sum('abandon_ph_score'), chang_trade_num = sum('chang_trade_num'),\
                chang_trade_score = sum('chang_trade_score')).values('newadd_num','newadd_score',\
                'pay_num', 'pay_score','supple_num','supple_score','supple_ph_num','supple_ph_score',\
                'chang_ph_num','chang_ph_score', 'chang_other_num','chang_other_score', 'abandon_ph_num',\
                'abandon_ph_score', 'chang_trade_num','chang_trade_score','xb','check_date')
        else:
            query_detail = self.get_queryset().filter(op_unit_name = unit_name,check_date__gte = now_day\
                ).values('xb','check_date').annotate(newadd_num = sum('newadd_num'),\
                newadd_score = sum('newadd_score'),pay_num = sum('pay_num'), pay_score = sum('pay_score'), \
                supple_num = sum('supple_num'),supple_score = sum('supple_score'),supple_ph_num = sum('supple_ph_num'), \
                supple_ph_score = sum('supple_ph_score'), chang_ph_num = sum('chang_ph_num'),\
                chang_ph_score = sum('chang_ph_score'), chang_other_num = sum('chang_other_num'),\
                chang_other_score = sum('chang_other_score'), abandon_ph_num = sum('abandon_ph_num'),\
                abandon_ph_score = sum('abandon_ph_score'), chang_trade_num = sum('chang_trade_num'),\
                chang_trade_score = sum('chang_trade_score')).values('newadd_num','newadd_score',\
                'pay_num', 'pay_score','supple_num','supple_score','supple_ph_num','supple_ph_score',\
                'chang_ph_num','chang_ph_score', 'chang_other_num','chang_other_score', 'abandon_ph_num',\
                'abandon_ph_score', 'chang_trade_num','chang_trade_score','xb','check_date')
        return query_detail


######======================================================================
class coTrade(models.Model):
    op_unit_name = models.CharField("运营单位",max_length = 20,null = True)
    day_score = models.IntegerField("每日积分", null = True)
    date = models.DateField("积分日期", null = True)
    class Meta:
        db_table = "index_co_trade"
        verbose_name = "运营单位积分趋势"

# 大部积分趋势表
class dpartTrade(models.Model):
    op_unit_name = models.CharField("运营单位", max_length = 20, null = True)
    dpart = models.CharField("大部", max_length = 20, null = True)
    day_score = models.IntegerField("每日积分",null = True)
    date = models.DateField("积分日期",null = True)

    class  Meta:
        db_table = "index_dp_trade"
        verbose_name = "大部积分趋势图"

class monthGoal(models.Model):
    op_unit_name = models.CharField("运营单位", max_length = 20, null = True)
    goal_date = models.DateField("积分日期",null = True)
    avg_score_goal = models.IntegerField("人月目标积分",null = True)

    class Meta:
        db_table = "index_month_goal"
        verbose_name = "月度人均目标积分"


class all(models.Model):
    objects = models.Manager()
    orm_objects = allManager()
    op_unit_name = models.CharField(max_length=255, blank=True, null=True)
    db = models.CharField(db_column='DB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    xb = models.CharField(db_column='XB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sale_name = models.CharField(max_length=255, blank=True, null=True)
    sale_num = models.CharField(max_length=255, blank=True, null=True)
    deadline_date = models.CharField(max_length=10, blank=True, null=True)
    his_all_score = models.FloatField(blank=True, null=True)
    his_cost_score = models.FloatField(blank=True, null=True)
    today_score = models.FloatField(blank=True, null=True)
    today_cost_score = models.FloatField(blank=True, null=True)
    score_balance = models.FloatField(blank=True, null=True)
    this_month_score = models.FloatField(blank=True, null=True)
    this_month_cost_score = models.FloatField(blank=True, null=True)
    g_pdate = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = "index_all"
        verbose_name = "累计积分汇总表（同步）"


class daily(models.Model):
    objects = models.Manager()
    orm_objects = dailyManager()
    op_unit_name = models.CharField(max_length=255, blank=True, null=True)
    db = models.CharField(db_column='DB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    xb = models.CharField(db_column='XB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sale_name = models.CharField(max_length=255, blank=True, null=True)
    sale_num = models.CharField(max_length=255, blank=True, null=True)
    check_date = models.CharField(max_length=10, blank=True, null=True)
    newadd_num = models.FloatField(blank=True, null=True)
    newadd_score = models.FloatField(blank=True, null=True)
    pay_num = models.FloatField(blank=True, null=True)
    pay_score = models.FloatField(blank=True, null=True)
    supple_num = models.FloatField(blank=True, null=True)
    supple_score = models.FloatField(blank=True, null=True)
    supple_ph_num = models.FloatField(blank=True, null=True)
    supple_ph_score = models.FloatField(blank=True, null=True)
    chang_ph_num = models.FloatField(blank=True, null=True)
    chang_ph_score = models.FloatField(blank=True, null=True)
    chang_other_num = models.FloatField(blank=True, null=True)
    chang_other_score = models.FloatField(blank=True, null=True)
    abandon_ph_num = models.FloatField(blank=True, null=True)
    abandon_ph_score = models.FloatField(blank=True, null=True)
    chang_trade_num = models.FloatField(blank=True, null=True)
    chang_trade_score = models.FloatField(blank=True, null=True)
    today_score = models.FloatField(blank=True, null=True)
    g_pdate = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        db_table = "index_daily"
        verbose_name = "每日积分明细(同步)"


# 大部积分明细表
class DpartDetail(models.Model):
    dpart = models.CharField("大部",max_length = 10,null = False)
    crews = models.IntegerField("人数",null= True)
    add_num = models.IntegerField("新增线索",null= True)
    supple_tels = models.IntegerField("补充电话数量", null = True)
    supple_num = models.IntegerField("批量增补", null = True)
    change_tels = models.IntegerField("修正电话", null = True)
    chang_other = models.IntegerField("修正其他数量", null = True)
    abandon_tels = models.IntegerField("废弃电话数量",null = True)
    change_trade = models.IntegerField("修改行业数量", null = True)
    pay_num = models.IntegerField("线索贡献到款", default = 0)
    score_sum = models.IntegerField("总积分", default = 0)
    month_goal = models.IntegerField("月度目标积分", default = 0)
    completion_rate = models.FloatField("完成率", null = True)
    reach_rate = models.FloatField("达标率", null = True)
    vaild_rank = models.IntegerField("可用积分", null = True)

    class Meta:
        db_table = "index_big_depart_data"
        verbose_name = "大部积分明细表"


# 小部积分明细
class SpartDetail(models.Model):
    spart = models.CharField("小部", max_length = 10, null = False)
    crews = models.IntegerField("人数",null= True)
    add_num = models.IntegerField("新增线索",null= True)
    supple_tels = models.IntegerField("补充电话数量", null = True)
    supple_num = models.IntegerField("批量增补", null = True)
    change_tels = models.IntegerField("修正电话", null = True)
    chang_other = models.IntegerField("修正其他数量", null = True)
    abandon_tels = models.IntegerField("废弃电话数量",null = True)
    change_trade = models.IntegerField("修改行业数量", null = True)
    pay_num = models.IntegerField("线索贡献到款", default = 0)
    score_sum = models.IntegerField("总积分", default = 0)
    month_goal = models.IntegerField("月度目标积分", default = 0)
    completion_rate = models.FloatField("完成率", null = True)
    reach_rate = models.FloatField("达标率", null = True)
    vaild_rank = models.IntegerField("可用积分", null = True)

    class Meta:
        db_table = "index_small_depart_data"
        verbose_name = "小部积分明细表"


# 个人积分排名
class Intergral_rank(models.Model):
    spart = models.CharField(max_length = 10, null = False)
    sale_name = models.CharField(max_length = 10, null = True)
    month_rank = models.IntegerField(default = 0)

    class Meta:
        db_table = "index_intergral_rank"
        verbose_name = "个人积分排名"

# 个人每日积分明细（月度积分直接group）
class personalScore(models.Model):
    op_unit_name = models.CharField("运营单位", max_length = 20, null = False)
    dpart = models.CharField("大部", max_length = 10, null = False)
    spart = models.CharField("小部", max_length = 10, null = False)
    sale_name = models.CharField("销售人员", max_length = 20, null = False)
    sale_num = models.CharField("人员编号", max_length = 20, null = False)
    check_date = models.DateField("明细积分日期", null = True)
    add_num = models.IntegerField("新增线索",null= True)
    add_score = models.IntegerField("新增积分", null = True)
    supple_tels = models.IntegerField("补充电话数量", null = True)
    supple_tels_score = models.IntegerField("补充电话积分",null = True)
    supple_num = models.IntegerField("批量增补", null = True)
    supple_score = models.IntegerField("增补积分", null = True)
    change_tels = models.IntegerField("修正电话", null = True)
    change_tels_score = models.IntegerField("修正电话积分", null = True)
    chang_other = models.IntegerField("修正其他数量", null = True)
    chang_other_score = models.IntegerField("修正其他积分", null = True)
    abandon_tels = models.IntegerField("废弃电话数量",null = True)
    abandon_tels_score = models.IntegerField("废弃电话积分",null = True)
    change_trade = models.IntegerField("修改行业数量", null = True)
    change_trade_score = models.IntegerField("修改行业积分", null = True)
    pay_num = models.IntegerField("线索贡献到款数量", default = 0)
    pay_num_score = models.IntegerField("线索贡献到款积分", default = 0)
    day_score = models.IntegerField("当日积分", default = 0)
    month_score = models.IntegerField("当月积分", default = 0)
    month_cost_score = models.IntegerField("当月兑换积分", null = True)


class big_depart_data(models.Model):
    big_department_name = models.CharField(max_length=5)
    month_score = models.IntegerField()
    month_score_finish = models.IntegerField()
    big_count = models.IntegerField()
    big_count_finish = models.IntegerField()
    new_tel = models.IntegerField()
    supplement_tel = models.IntegerField()
    correct_tel = models.IntegerField()
    correct_cule = models.IntegerField()
    abandon_tel = models.IntegerField()
    success_num =  models.IntegerField()
    all_score = models.IntegerField()
    people_avarage_score = models.FloatField()
    today_avarage = models.FloatField()
    yesterday_avarage = models.FloatField()

    class Meta:
        db_table = "big_depart_data"
        verbose_name = "大部积分"


class new(models.Model):
    op_unit_name = models.CharField(max_length=255,blank=True,null=True)
    db = models.CharField(db_column='DB', max_length=255, blank=True, null=True)
    xb = models.CharField(db_column='XB', max_length=255, blank=True, null=True)
    sale_name = models.CharField(max_length=255, blank=True, null=True)
    pg_cust_id = models.CharField(max_length=255, blank=True, null=True)
    full_info = models.CharField(max_length=255, blank=True, null=True)
    pg_cust_type = models.CharField(max_length=255, blank=True, null=True)
    pg_cust_status = models.CharField(max_length=255, blank=True, null=True)
    hint_src_id_1 = models.CharField(max_length=255, blank=True, null=True)
    city_id = models.CharField(max_length=255, blank=True, null=True)
    create_post_id = models.CharField(max_length=255, blank=True, null=True)
    create_user_id = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    audit_time = models.DateTimeField(blank=True, null=True)
    audit_result_id = models.CharField(max_length=255, blank=True, null=True)
    audit_result_value = models.CharField(max_length=255, blank=True, null=True)
    protect_time = models.DateTimeField(blank=True, null=True)
    un_protect_time = models.DateTimeField(blank=True, null=True)
    newadd_type = models.CharField(max_length=255, blank=True, null=True)
    pos_name = models.CharField(max_length=255, blank=True, null=True)
    checkornot = models.CharField(max_length=255)
    checking_result = models.CharField(max_length=255)
    whyturndown = models.CharField(max_length=255)
    check_man = models.CharField(max_length=255)
    check_date = models.CharField(max_length=255)
    remark = models.CharField(max_length=255, blank=True, null=True)
    g_pdate = models.CharField(max_length=10)

    class Meta:
        db_table = "index_new"
        verbose_name = "新增明细"

class add(models.Model):
    op_unit_name = models.CharField(max_length=255, blank=True, null=True)
    db = models.CharField(db_column='DB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    xb = models.CharField(db_column='XB', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sale_name = models.CharField(max_length=255, blank=True, null=True)
    pg_cust_id = models.CharField(max_length=255, blank=True, null=True)
    full_info = models.CharField(max_length=255, blank=True, null=True)
    full_info_status = models.CharField(max_length=255, blank=True, null=True)
    contact_type = models.CharField(max_length=255, blank=True, null=True)
    pg_cust_type = models.CharField(max_length=255, blank=True, null=True)
    pg_cust_status = models.CharField(max_length=255, blank=True, null=True)
    city_id = models.CharField(max_length=255, blank=True, null=True)
    cust_create_post_id = models.CharField(max_length=255, blank=True, null=True)
    cust_create_pos_name = models.CharField(max_length=255, blank=True, null=True)
    cust_create_time = models.DateTimeField(blank=True, null=True)
    cust_create_user_id = models.CharField(max_length=255, blank=True, null=True)
    full_info_create_time = models.DateTimeField(blank=True, null=True)
    full_info_create_user_id = models.CharField(max_length=255, blank=True, null=True)
    full_info_create_pos_name = models.CharField(max_length=255, blank=True, null=True)
    pdate = models.CharField(max_length=10, blank=True, null=True)
    checkornot = models.CharField(max_length=255)
    checking_result = models.CharField(max_length=255)
    whyturndown = models.CharField(max_length=255)
    check_man = models.CharField(max_length=255)
    check_date = models.CharField(max_length=255)
    remark = models.CharField(max_length=255, blank=True, null=True)
    g_pdate = models.CharField(max_length=10)


class change(models.Model):
    op_unit_name = models.TextField(blank=True, null=True)
    db = models.TextField(db_column='DB', blank=True, null=True)  # Field name made lowercase.
    xb = models.TextField(db_column='XB', blank=True, null=True)  # Field name made lowercase.
    sale_name = models.TextField(blank=True, null=True)
    change_id = models.TextField(blank=True, null=True)
    change_type = models.TextField(blank=True, null=True)
    pg_cust_id = models.TextField(blank=True, null=True)
    change_item = models.TextField(blank=True, null=True)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    whychange = models.TextField(blank=True, null=True)
    changeremark = models.TextField(blank=True, null=True)
    checkingremark = models.TextField(blank=True, null=True)
    pos_id = models.TextField(blank=True, null=True)
    pos_name = models.TextField(blank=True, null=True)
    chang_time = models.TextField(blank=True, null=True)
    checking_result = models.TextField(blank=True, null=True)
    check_pos = models.TextField(blank=True, null=True)
    check_man_pos = models.TextField(blank=True, null=True)
    check_time = models.TextField(blank=True, null=True)
    supple_ph = models.SmallIntegerField(blank=True, null=True)
    chang_ph = models.SmallIntegerField(blank=True, null=True)
    chang_other = models.SmallIntegerField(blank=True, null=True)
    abandon_ph = models.SmallIntegerField(blank=True, null=True)
    check_man = models.TextField(blank=True, null=True)
    g_pdate = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = "index_change"
        verbose_name = "变更单明细"


