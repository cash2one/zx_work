#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.shortcuts import render
from models import *
from datetime import datetime
import datetime as d_time
# Create your views here.
# get all areas' score
# 工作日完成进度
now_day = datetime.now().date()
lastday = calendar.monthrange(now_day.year,now_day.month)[1]
start_day = datetime.strptime(datetime.strftime(now_day,'%Y-%m') + '-01','%Y-%m-%d')
end_day = datetime.strptime(datetime.strftime(now_day,'%Y-%m')+ '-'+str(lastday),'%Y-%m-%d')
# 计算当月总工作日，当月到目前为止工作日
def isWeekday(start_day,now):
    now_weekday = 0
    month_weekday = 0
    for day in range((end_day-start_day).days):
        if start_day.weekday() not in (5,6):
            month_weekday += 1
        start_day = start_day + d_time.timedelta(1)
    for day in range((now-start_day).days):
        if start_day.weekday() not in (5,6):
            now_weekday += 1
        start_day = start_day + d_time.timedelta(1)
    return [now_weekday,month_weekday]


# 返回 大部小部 人员数和 运营单位月目标积分，
def dpGoalNum(op_unit_name):
    goal_date = datetime.strftime(datetime.now(),'%Y-%m') + '-01'
    # 获取大部人员数和人均积分
    dp_man_nums = all.objects.row("select db,count(*) as man from all where op_unit_name = '%s' group by db")%op_unit_name
    # 获取小部人员数
    sp_man_nums = all.objects.row("select xb,count(*) as man from all where op_unit_name = '%s' group by xb")%op_unit_name
    # avg goal score of everymonth
    person_goal = goal.objects.row("select avg_score_goal from avg_goal where goal_date = %s,op_unit_name = %s")% (goal_date,op_unit_name)
    weekday = isWeekday(goal_date,datetime.now())
    now_weekday = weekday[0]
    month_weekday = weekday[1]
    # 大部，大部人数；小部，小部人数；整个运营单位的人均月目标；到当前的工作日，一个月的工作日
    goal_dict = {'dp_man_nums':dp_man_nums,'sp_man_nums':sp_man_nums,'person_goal':person_goal[0],\
        'now_weekday':now_weekday,'month_weekday':month_weekday}
    return goal_dict

def index(request):
    return render(request, 'index.html')

# 大部一周期每日积分
def dpDayScore(request):
    return render(request,'index.html')

# 大部小部积分明细,大部趋势
def detailScore(request):
    # 大部趋势数据
    # 小部积分 达标率，完成率，目标积分，总积分，可用积分+各种明细
    # 大部积分 达标率，完成率，目标积分，总积分，可用积分+各种明细
    #co_trade_exist = coTrade.objects.one()  # 运营单位趋势表是否有内容
    #origin_day_value = [0 for i in range(1,days+1)]
    """大部趋势图数据"""
    #
    #
    #
    ######## op_unit_name = request.??
    dp_trade_exist = dpartTrade.objects.one() # 大部趋势表是否有内容
    dp_trade = all.orm_objects.get_co_trade(dp_trade_exist,op_unit_name)
    this_month_day = int(calendar.monthrange(now_day.year,now_day.month)[1])
    first_day = datetime.strftime(datetime.now(),"%Y-%m")+'-01'
    days = range(1,this_month_day+1)
    trade_value = {}
    part_list = [] # 大部列表
    for i in dp_trade:
        if not i['dpart'] in part_list:
            part_list.append(i['part'])
        else:continue

    # trade_value:{"广州":[1,2,3,4,5,67,...],"深圳":[2,32,43,545,65,234,12,123,34]}
    for dp in part_list:
        trade_value[dp] = []
        for obj in dp_trade:
            if dp != obj['dpart']:
                continue
            else:
                trade_value[dp].append(obj['today_score'])
    '''大部趋势图数据'''

    ''' 小部积分明细 '''
    # 大部，大部人数；小部，小部人数；整个运营单位的人均月目标；到当前的工作日，一个月的工作日
    # goal_dict = {'dp_man_nums':dp_man_nums,'sp_man_nums':sp_man_nums,'person_goal':person_goal,\
    #     'now_weekday':now_weekday,'month_weekday':month_weekday}
    goal_dict = dpGoalNum(op_unit_name)
    man_goal = goal_dict['person_goal'] # 该运营单位的月人均目标

    sp_detail_exist = SpartDetail.objects.one() # 小部积分明细是否有内容
    sp_detail = daily.orm_objects.get_sp_detail(sp_detail_exist,op_unit_name)
    sp_man_real = all.orm_objects.get_sp_reach_all(sp_detail_exist,op_unit_name) # 小部人数 当月积分
    sp_summary = []
    for summary in sp_man_real:
        man_num = summary.man_num
        man_reach = all.objects.filter(op_unit_name = op_unit_name,this_month_score__gte=man_goal,\
            spart = summary.spart).all()
        sp = {}
        sp['spart'] = summary.spart
        sp['reach_rate'] = round(float(len(man_reach)*100)/float(man_num),1)
        sp['comp_rate'] = round(float(summary.this_month_score*100)/float(man_goal*man_num),1)
        sp['vaild'] = all.orm_objects.get_sp_vaild(sp_detail_exist,op_unit_name,summary.spart)[0]['vaild_rank']
        sp['month_goal'] = summary.man_num * man_goal
        sp['month_score'] = summary.this_month_score
        sp_summary.append(sp)
    # 今日的小部积分数据 sp_score:{'xb1':{"":'',"":''}.'xb2':{"":''}}
    ''' 小部积分明细 '''

    ''' 大部积分明细 '''
    dp_detail_exist = DpartDetail.objects.one() # 大部积分明细表是否有内容
    dp_detail = daily.orm_objects.get_sp_detail(dp_detail_exist,op_unit_name)
    dp_summary = all.orm_objects.get_dp_reach_all(dp_detail_exist,op_unit_name)
    dp_summary = []
    for summary in dp_summary:
        dp['dpart'] = summary.dpart
        dp['reach_rate'] = round(float(man_reach*100)/float(man_num),1)
        dp['comp_rate'] = round(float(summary.this_month_score*100)/float(man_goal*man_num),1)
        dp['vaild'] = all.orm_objects.get_dp_vaild(dp_detail_exist,op_unit_name,summary.dpart)[0]['vaild_rank']
        dp['month_goal'] = summary.man_num*man_goal
        dp['month_score'] = summary.this_month_score
    print this_month_day,'-------------'
    return render(request,'index.html',{
        'dp_detailscore':dp_score,
        'dp_summary':dp_summary,
        'sp_detailscore':sp_detail,
        'sp_summary':sp_summary,
        'db_trade':trade_value,
        'this_month':this_month_day
        })


# 个人当前积分排名
def personalRank(request):
    return render(request,'person_rank.html',{'personal_rank':rank})

# 个人积分明细
def personalDetail(request):
    return render(request,'person_dailydetail.html',{'personal_detail':detail})

# 个人新增明细
def personalNew(request):
    return render(request,'person_new.html')

# 首页刷新缓存：大部积分明细/小部积分/个人积分的计算存入数据库 + 运营单位每月每日积分趋势的计算和显示
def homepage(request):

    return render(request,'all_co.html')

'''
url = urlparse.urljoin('/focus/', article_id)
return redirect(url)
def index(request):
    name_list = Polls.objects.all()
    result = []

    for obj in name_list:
        a_dict = {'index':obj.index,'name':obj.name}
        result.append(a_dict)
    print result
    return render(request,'index.html',{'result':result})
'''

