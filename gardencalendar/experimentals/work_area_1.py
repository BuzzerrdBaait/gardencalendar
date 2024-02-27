from datetime import date
import datetime
import calendar
from json import dumps

def get_calendar_days_and_months():
        
        month_dictionary={
                    1:'January',
                    2:'February',
                    3:'March',
                    4:'April',
                    5:'May',
                    6:'June',
                    7:'July',
                    8:'August',
                    9:'September',
                    10:'October',
                    11:'November',
                    12:'December',
                }

        day_dictionary={
                    0:'Monday',
                    1:'Tuesday',
                    2:'Wednesday',
                    3:'Thursday',
                    4:'Friday',
                    5:'Saturday',
                    6:'Sunday',
                }
        
        today_data=date.today()

        year=today_data.year

        last_year=year-1

        month=today_data.month

        today=today_data.day

        day_of_week_int=today_data.weekday()

        day_of_week=day_dictionary[day_of_week_int]

        month_str=month_dictionary[month]

        blank_days=[]
        num_days_in_month=[]
        correlating_year=[]
        str_month=[]
        dates_list=[]
        dates_list_list=[]

        for i in range(1,4):
            for x in range(1,13):
                month_info=calendar.monthrange(last_year,x)
                blank_days.append(month_info[0])
                num_days_in_month.append(month_info[1])
                correlating_year.append(last_year)
                str_month.append(month_dictionary[x])

                dates_list.clear()

                for days in range(1,month_info[1]):
                    dates=datetime.date(last_year,x,days)
                    dates_str=dates.strftime('%Y-%m-%d')
                    dates_list.append(dates_str)
            
                dates_list_list.append(dates_list.copy())
 
            last_year+=1

        return(blank_days,num_days_in_month,correlating_year,str_month,dates_list_list)
            
date_info=get_calendar_days_and_months()

master_list=[]

def find_todays_date_and_index():
    today_data=date.today()
    for index,sublist in enumerate(date_info[4]):
        if today_data.strftime('%Y-%m-%d') in sublist:
            print(f'TODAY IS FOUND {today_data} at {index}')
            return(index,todays_data)
    return()

def make_master_list():
    for item in range(0,len(date_info[0])):
            date_tuple=(date_info[0][item], date_info[1][item], date_info[2][item],date_info[3][item])
            master_list.append(date_tuple)

make_master_list()

todays_index=find_todays_date_and_index()

todays_data=master_list[todays_index]

num_blank_days=(date_info[0][todays_index])

num_days_in_this_month=(date_info[1][todays_index])

this_year_is=(date_info[2][todays_index])

this_month_is=(date_info[3][todays_index])

dates_in_this_month=(date_info[4][todays_index])

print(f"this month is {this_month_is}")

print(f"the dates in this month are..{dates_in_this_month}")



"""
today_data=date.today()
year=today_data.year
last_year=year-1
month=today_data.month
blank_days=date_info[0]
num_days_in_month=date_info[1]
correlating_year=date_info[2]
str_month=date_info[3]
"""





