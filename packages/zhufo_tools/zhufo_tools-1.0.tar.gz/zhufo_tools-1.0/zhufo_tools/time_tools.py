#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime

from zhufo_tools.logger import MyLogger

prolog = MyLogger("time_tools_log", level=20).logger


class TimeTools:

    @staticmethod
    def get_now():
        """
        获取当前时间格式yyyy-mm-dd hh:mm:ss
        '2022-06-13 16:40:31'
        :return:
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_day():
        """
        获取今日日期
        :return:
        """
        return TimeTools.get_now()[:10]

    @staticmethod
    def get_now_special_bef_aft(days=0, hours=0, now='', h_m_s='00:00:00'):
        """
        获取指定时间点前后时间间隔的时间, 可指定返回时刻值h_m_s
        :param days: 正数代表：几天前，负数反之
        :param hours:正数代表：几小时前，负数反之
        :param now: 指定时间，默认今日，格式：yy-mm-dd
        :param h_m_s:指定时刻，默认'00:00:00'
        :return:
        """
        if now == '':
            now = datetime.datetime.now()
        else:
            now = datetime.datetime.strptime(now, '%Y-%m-%d')
        other_style_time = now - datetime.timedelta(days=days, hours=hours)
        other_style_time = other_style_time.strftime("%Y-%m-%d ")
        other_style_time += h_m_s
        return other_style_time

    @staticmethod
    def get_now_bef_aft(days=0, hours=0, now='', minutes=0, seconds=0):
        """
        获取当前时间点前后时间间隔的时间
        :param days:正数代表：几天前，负数反之
        :param hours:正数代表：几小时前，负数反之
        :param now:指定时间，默认当前时间，格式：yy-mm-dd hh:mm:ss
        :param minutes:正数代表：几分钟前，负数反之
        :param seconds:正数代表：几秒总前，负数反之
        :return:
        """
        if now == '':
            now = datetime.datetime.now()
        else:
            now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        other_style_time = now - datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        other_style_time = other_style_time.strftime("%Y-%m-%d %H:%M:%S")
        return other_style_time

    @staticmethod
    def get_day_value(time1: datetime.datetime, time2: datetime.datetime):
        """
        获取两个时间的差值
        :param time1:
        :param time2:
        :return:
        """
        return (time1 - time2).days

    @staticmethod
    def timestamp2time(timestamp):
        """
        时间戳转时间，格式：yy-mm-dd hh:mm:ss
        :param timestamp:
        :return:
        """
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    @staticmethod
    def time2timestamp(time_str, time_format="%Y-%m-%d %H:%M:%S") -> float:
        """
        时间转时间戳
        :param time_str:
        :param time_format:yy-mm-dd hh:mm:ss 默认
        :return:
        """
        # 字符串转结构时间
        struct_time = time.strptime(time_str, time_format)
        # 结构时间转时间戳
        timestamp = time.mktime(struct_time)
        return timestamp

    @staticmethod
    def get_date_range(begin_date, end_date, order: bool = True) -> list:
        """
        获取日期区间列表，包含首尾日期
        :param begin_date:起始日期，格式：yyyy-mm-dd
        :param end_date:结束日期，格式：yyyy-mm-dd
        :param order:是否正序，默认正序
        :return:
        """
        # 转化对象
        _begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
        _end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        date_range = [
            TimeTools.get_now_special_bef_aft(days=i, now=end_date)[:10]
            for i in range((_end_date - _begin_date).days, -1, -1)
        ]
        # 是否逆序
        if not order:
            date_range.reverse()
        return date_range


def test_case():
    """
    实例测试
    :return:
    """
    # 获取今日日期-->2021-05-10
    print(TimeTools.get_day())
    # 获取当前时间-->2021-05-10 11:56:45
    print(TimeTools.get_now())

    # 获取明天的14:00:00
    print(TimeTools.get_now_special_bef_aft(days=-1, h_m_s="14:00:00"))
    # 获取2021-05-10 13:37:00一小时后
    print(TimeTools.get_now_bef_aft(hours=-1, now="2021-05-10 13:37:00"))

    # 比较两个datetime.datetime类型时间间隔【datetime.datetime(年, 月, 日)】
    print(TimeTools.get_day_value(datetime.datetime(2021, 3, 1), datetime.datetime(2021, 3, 2)))
    # 时间戳转时间，格式yy-mm-dd hh:mm:ss
    print(TimeTools.timestamp2time(1620625704.778211))
    print(TimeTools.time2timestamp("2021-05-10 13:48:24"))
    # 逆序打印2021-07-01至2021-07-15间日期区间列表
    print(TimeTools.get_date_range(begin_date="2021-07-01", end_date="2021-07-15", order=False))


if __name__ == "__main__":
    test_case()
