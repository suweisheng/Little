# encoding: utf8

import time
import datetime
import math


# 夏令时，也叫夏时制，又称“日光节约时制”和“夏令时间”，是一种为节约能源而人为规定地方时间的制度，
# 在这一制度实行期间所采用的统一时间称为“夏令时间”。
# 一般在天亮早的夏季人为将时间调快一小时，可以使人早起早睡，减少照明量，以充分利用光照资源，从而节约照明用电。
# 各个采纳夏时制的国家具体规定不同。全世界有近110个国家每年要实行夏令时。
# 我国实行夏令时的时间是1986-1991年，每年4月的第2个星期日早上2点到9月的第2个星期日早上2点之间，1992年后暂停实行

# UTC, 协调世界时，又称世界统一时间、世界标准时间、国际协调时间
# 协调世界时是以原子时秒长为基础，在时刻上尽量接近于世界时（地球自转的变化）的一种时间计量系统，相差不会超过0.9秒。
# 这套时间系统被应用于许多互联网和万维网的标准中，例如，网络时间协议就是协调世界时在互联网中使用的一种方式
# 在时刻上尽量接近世界时的一种时间计量系统。它的出现是现代社会对于精确计时的需要
# 中国大陆、中国香港的时间与UTC的时差均为+8，也就是UTC+8

# GMT，格林尼治标准时间，它以格林尼治天文台的经线为0 度经线，将世界分为24 个时区，东区加, 西区减
# 为了方便，在不需要精确到秒的情况下，通常将GMT 和UTC 视作等同，但UTC 更加科学更加精确

# 起始时间戳(0), 起始GMT、UTC时间，1970-01-01 00:00:00

def main():
    time.sleep(0) # 让进程睡眠，单位秒，参数可以是浮点数以指示更精确的睡眠时间

    print time.time() # 返回当前本地系统时间戳，返回以秒为单位的浮点数
    print math.floor(time.time())
    print int(time.time())

    # struct_time 类 是一个元组，以下函数返回的都是一个 struct_time 对象, 可以通过 ret[0], ret.tm_year 获取元素
    # 0   tm_year     (for example, 1993)
    # 1   tm_mon      range [1, 12]
    # 2   tm_mday     range [1, 31]
    # 3   tm_hour     range [0, 23]
    # 4   tm_min      range [0, 59]
    # 5   tm_sec      range [0, 61]
    # 6   tm_wday     range [0, 6], Monday is 0
    # 7   tm_yday     range [1, 366]
    # 8   tm_isdst    0, 1 or -1
    # 以下函数的返回结果都是 struct_time 对象
    t = (1970, 1, 1, 8, 0, 0, 3, 1, 0)
    print time.struct_time(t)
    print time.gmtime(1664446238)
    print time.gmtime() # 将时间戳转换成 UTC格式 struct_time, 参数默认当前时间戳，0时区，把UTC时间转换成北京时间的话，需要小时数加上8
    print time.localtime() # 将时间戳转换成 本地格式 struct_time, 参数默认当前时间戳
    print time.strptime("2022 9 29 Nov", "%Y %m %d %b")  # 默认"%a %b %d %H:%M:%S %Y"

    # 格式化时间戳, 接收 struct_time 对象，按照格式化字符串
    # %Y 年; %m 月; %d 日; %H %I 时; %M 分; %S 秒; %w 星期(周日0); %p AM或PM
    # %j 一年中的第几天;
    # %b 语言环境的缩写月份名称
    # %a 缩写工作日名称
    # %W 一年的第几周（周一为一周的开始; %U 一年的第几周（周一为一周的开始）
    # %c %x %X 根据本地环境适当的日期时间显示，如 09/29/22 09:50:28
    print time.strftime("%Y-%m-%d %H:%M:%S ", time.gmtime())
    print time.strftime("%a %b")
    print time.strftime("%x")
    print time.strftime("%X")
    print time.strftime("%c")

    # 返回当前适当日期时间字符串
    print time.asctime(time.gmtime()) # Thu Sep 29 18:15:51 2022

    # 返回一个本地时间戳，不是UTC,mktime 输入的日期是带时区的，返回的值才是不带时区的,是localtime的反函数
    # 后面3个参数可以不计算，直接指定为0不影响结果
    t = (1970, 1, 1, 8, 0, 0, 3, 1, 0)
    print time.mktime(t)

def test_datetime():
    # print datetime.MINYEAR, datetime.MAXYEAR # 支持的最小最大年

    # ================== date 对象
    # date = datetime.date
    # date(2022, 10, 15) # 自定义date对象
    # today = date.today() # 表示今日的date对象

    # print today.year, today.month, today.day # int
    # print today.replace(month=1) # 替换指定参数得到新date对象

    # print today.toordinal() # 当前日期的序数(第几天) 初始值为1 即date(1, 1, 1)
    # print date(2022, 10, 15).toordinal() - (date(2022, 10, 15).replace(month=1, day=1).toordinal()) # 计算一年中的第几天
    # print today.weekday() # 周几 0-6 周一~周日
    # print today.isoweekday() # 周几1-7 周一~周日
    # print today.isocalendar() # 返回一个元表 (年, 一年中的第几周, 周几)
    # print today.isoformat() # 标准日期字符串
    # print today.ctime() # 标准日期字符串 C标准
    # print today.strftime("%Y-%m-%d %H:%M:%S")
    # print today.timetuple() # return struct_time


    # ================== time 对象
    # time = datetime.time
    # time(14, 29, 21, 100000) # 自定义time对象,精确到微妙
    # today = datetime.datetime.today().time() # 表示今日的time对象 

    # print today.hour, today.minute, today.second, today.microsecond
    # print today.replace(second=10)

    # print today.isoformat() # HH:MM:SS.xx
    # print today.strftime("%H:%M:%S")


    # ================== timedelta 对象
    # 将两个date、time或datetime实例之间的差异表示为微秒分辨率的持续时间
    timedelta = datetime.timedelta
    delay = timedelta(5, 6, 10, 3, 1000)  # 自定义timedelta对象,精确到微妙
    delay = timedelta(days=365)

    print delay.total_seconds() # 返回持续时间的总秒数
    print delay.days, delay.seconds # 返回持续时间的天, 秒数

    # t1 = datetime.date(2022, 10, 16); t2 = datetime.date(2022, 10, 17)
    # t1 = datetime.datetime(2022, 10, 15, 14, 29, 21); t2 = datetime.datetime(2022, 10, 16, 14, 30, 22)
    # delay = t2 - t1
    
    year = timedelta(days=365)
    ten_years = (year * 10)
    three_years = (ten_years - year) // 3
    print abs(three_years - ten_years) == (2 * three_years + year)



    # ================== datetime 对象 (date 和 time 的合体)
    # datetime1 = datetime.datetime
    # today = datetime1.today() # 表示今日的datetime对象 相同效果 datetime.fromtimestamp(time.time()
    # today = datetime1.fromtimestamp(time.time()) # 根据时间戳构造
    # datetime1(2022, 10, 15, 14, 29, 21, 100000) # 自定义datetime对象,精确到微妙
    # datetime1.fromordinal(25) # 根据日期序数构造 0001-01-25 00:00:00

    # print today.toordinal() # 当前日期的序数(第几天)
    # print today.weekday() # 周几 0-6 周一~周日
    # print today.isoweekday() # 周几1-7 周一~周日
    # print today.isocalendar() # 返回一个元表 (年, 一年中的第几周, 周几)
    # print today.isoformat() # 标准日期字符串 YYYY-MM-DDTHH:MM:SS
    # print today.ctime() # 标准日期字符串 C标准 Wed Oct 12 15:00:55 2022
    # print today.strftime("%Y-%m-%d %H:%M:%S") # 格式化输出
    # print today.timetuple() # return struct_time

    # print today.year, today.month, today.day
    # print today.hour, today.minute, today.second, today.microsecond
    # print today.replace(month=1) # 替换指定参数得到新datetime对象

    # print today.date() # 返回date对象
    # print today.time() # 返回time对象
    # print today.timetz() # 返回timetz对象



base_0 = int(time.mktime((2000, 1, 3, 0, 0, 0, 0, 0, 0)))
base_6 = int(time.mktime((2000, 1, 3, 6, 0, 0, 0, 0, 0)))
one_hort = 3600
one_day = 24 * one_hort
one_week = 7 * one_day

if time.localtime(base_0).tm_wday != 0 and time.localtime(base_6).tm_wday != 0:
    raise Exception("must be week 1")

def time_second():
    return int(time.time())

def time_millisecond():
    return int(time.time()*1000)

def format_time(ts=None):
    ts = ts if ts else time_second()
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))

def format_day(ts=None):
    ts = ts if ts else time_second()
    return time.strftime("%Y-%m-%d", time.localtime(ts))

def get_pass_day0(ts=None):
    ts = ts if ts else time_second()
    return int((ts - base_0) / one_day)

def get_pass_day6(ts=None):
    ts = ts if ts else time_second()
    return int((ts - base_6) / one_day)

def is_after(ts=None, hour=0):
    ts = ts if ts else time_second()
    return time.localtime(ts).tm_hour >= hour

def get_year(ts=None):
    ts = ts if ts else time_second()
    return time.localtime(ts).tm_year

def get_month(ts=None):
    ts = ts if ts else time_second()
    return time.localtime(ts).tm_mon

def get_day(ts=None):
    ts = ts if ts else time_second()
    return time.localtime(ts).tm_mday

def get_week(ts=None):
    ts = ts if ts else time_second()
    return time.localtime(ts).tm_wday

def get_hour(ts=None):
    ts = ts if ts else time_second()
    return time.localtime(ts).tm_hour

def get_minute(ts=None):
    ts = ts if ts else time_second()
    return time.localtime(ts).tm_min

def get_second(ts=None):
    ts = ts if ts else time_second()
    return time.localtime(ts).tm_sec

def get_day_second(ts=None):
    ts = ts if ts else time_second()
    return (ts - base_0) % one_day

def get_hour_begin0(ts=None):
    ts = ts if ts else time_second()
    return ts - (ts - base_0) % one_hort

def get_day_begin0(ts=None):
    ts = ts if ts else time_second()
    return ts - (ts - base_0) % one_day

def get_week_begin0(ts=None):
    ts = ts if ts else time_second()
    return ts - (ts - base_0) % one_week

def get_month_begin0(ts=None):
    ts = ts if ts else time_second()
    t = time.localtime(ts)
    return time.mktime([t[0], t[1], 1, 0, 0, 0, t[6], t[7], t[8]])

def get_year_begin0(ts=None):
    ts = ts if ts else time_second()
    t = time.localtime(ts)
    return time.mktime([t[0], 1, 1, 0, 0, 0, t[6], t[7], t[8]])

def get_next_day_begin0(ts=None):
    return get_day_begin0(ts) + one_day

def get_next_week_begin0(ts=None):
    return get_week_begin0(ts) + one_week

def get_next_month_begin0(ts=None):
    ts = ts if ts else time_second()
    t = time.localtime(ts)
    year = t[0]
    month = t[1]
    if t[1] == 12:
        year = year + 1
        month = 1
    else:
        month = month + 1
    return time.mktime([year, month, 1, 0, 0, 0, t[6], t[7], t[8]])

def date_to_ts(time_str):
    import re
    t = re.findall("\d+", time_str)
    if len(t) != 6:
        return 0
    t = map(int, t)
    return int(time.mktime([t[0], t[1], t[2], t[3], t[4], t[5], 0, 0, 0]))


if __name__ == "__main__":
    # main()
    test_datetime()
    # print format_time(get_year_begin0())