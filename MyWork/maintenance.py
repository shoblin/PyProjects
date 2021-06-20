# -------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      atopolskiy
#
# Created:     03.03.2021
# Copyright:   (c) atopolskiy 2021
# Licence:     <your licence>
# -------------------------------------------------------------------------------
import requests
import re

from datetime import datetime, timedelta
from pyzabbix import ZabbixAPI


NUM_DAY = '([1234])(?:st|nd|rd|th)'
WEEKDAY_NAME = '(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Everyday)'
TIME_ZONE = r'(\w{3})'
HOUR_MIN = r'(\d{2}:\d{2})'

WEEK_DAY_NUMERIC = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
    'Sunday': 7
}


def get_last_data_zabbix_connect():
    """
    Connect to zabbix and get last value of AGG_Windows_servers
    """

    zbxurl = 'https://zabbix.finam.ru/zabbix'
    zbxname = 'api-readonly-new'
    zbxpass = 'VRSFi*jl05%Yw%6qM}a'

    zapi = ZabbixAPI(zbxurl, user=zbxname, password=zbxpass)
    hosts = ['AGG_Windows_servers']

    last_data = zapi.item.get(output=['lastvalue'], search={'name': 'Список узлов с проблемой'}, selectHosts=hosts,
                              itemids=['1514319'], sortfield='name', startSearch=1)
    result = last_data[0]['lastvalue']

    return result


def read_hostnames():
    """
    Take names of hosts from zabbix
    """
    names = []
    last_data = get_last_data_zabbix_connect()
    last_data = last_data.strip()
    for line in last_data.split('\n'):
        name = line.split(',')[0]
        names.append(name)

    return names


def connect_jira():
    """
    Open connection to JIRA
    """
    options = {"server": "https://sd.finam.ru/"}
    login = 'tscontrol-p'
    password = 'v55cohFu'

    session = requests.Session()
    session.auth = (login, password)

    return session


def find_next_weekday(ndays, weekd):
    """
    Find next date
    """
    curr_day = datetime.now()
    curr_weekday = curr_day.isoweekday()
    weekday = WEEK_DAY_NUMERIC[weekd]
    first_day = curr_day.replace(day=1)

    #
    delta = (int(weekday) - int(curr_weekday)) % 7

    if delta == 0:
        delta = 7

    # If we don't have any
    if len(ndays) < 1:
        date = datetime.now() + timedelta(days=delta)
        return date
    else:
        while True:
            for n in ndays:
                wday = (weekday - first_day.isoweekday() + 7) % 7 + (int(n) - 1) * 7 + 1

                if curr_day < first_day.replace(day=wday):
                    return first_day.replace(day=wday)

            first_day = first_day.replace(month=first_day.month + 1)


def conv_time(tz, tz_time):
    """
    Convert time from other time zone into MSK
    Args:
        tz str: Time zone
        tz_time str: Time

    Returns:
        hours:minutes
    """
    tz_time = datetime.strptime(tz_time, '%H:%M')

    if tz == 'EST':
        tz_time = tz_time + timedelta(hours=7)

    return f"{tz_time.hour:02}:{tz_time.minute:02}"


def get_date(interval):
    """
    Take from interval numer of weekday, name of weekday, time
    """

    if interval == 'MSK Manual':
        return interval

    num_days = re.findall(NUM_DAY, interval)
    pattern = WEEKDAY_NAME + r'\s+' + TIME_ZONE + r'\s+' + HOUR_MIN + r'\s*-\s*' + HOUR_MIN
    pattern2 = WEEKDAY_NAME + r'\s+' + TIME_ZONE + r'\s+' + HOUR_MIN + r'\s*-\s*' + WEEKDAY_NAME + r'\s+' + HOUR_MIN

    if groups := re.search(pattern, interval):

        weekday, tz, intr_srt, intr_end = groups.groups()
        intr_srt, intr_end = conv_time(tz, intr_srt), conv_time(tz, intr_end)

        hours = intr_srt + '-' + intr_end

        # Find a next date
        # We can reboot server Everyday take date of next day
        if weekday == 'Everyday':
            date = datetime.now() + timedelta(days=1)
        # Find next date -> find_next_weekday()
        else:
            date = find_next_weekday(num_days, weekday)

        result = date.date().strftime('%d.%m.%Y') + ' ' + hours
        return result

    elif groups2 := re.search(pattern2, interval):
        weekday, tz, intr_srt, weekday2,  intr_end = groups2.groups()
        intr_srt, intr_end = conv_time(tz, intr_srt), conv_time(tz, intr_end)

        date = find_next_weekday(num_days, weekday)
        date2 = find_next_weekday([], weekday2)

        result = date.date().strftime('%d.%m.%Y') + ' ' + intr_srt
        result += '-' + date2.date().strftime('%d.%m.%Y') + ' ' + intr_end
        return result

    else:
        return interval


def parse_timestamp_from_response(date):
    try:
        date = date.split('-')[0]
        return datetime.strptime(date, '%d.%m.%Y %H:%M')
    except ValueError:
        return datetime.now() + timedelta(days=365)


def print_result(results):
    """
    """
    keys = sorted(list(results.keys()), key=parse_timestamp_from_response)
    print(keys)
    for key in keys:
        print('== ' + key + ' ==')
        for server, maint in results[key]:
            print(server, maint, sep=" *** ")
        print()


def main():

    session = connect_jira()

    # Find all hosts in Zabbix.
    name_list = read_hostnames()

    # Create iql
    iql = 'Name IN (' + ", ".join(name_list) + ')'

    # URLs for connection
    url = 'https://sd.finam.ru'
    api_url = url + '/rest/insight/1.0/iql/objects'

    params = [('objectSchemaId', 2), ('iql', iql), ('resultPerPage', 10000)]

    results = session.get(url=api_url, params=params).json()

    # Dictionary {maintain period : set with server's names}
    maint_hosts = {}

    for result in results['objectEntries']:
        host_name = result['label']
        for atr in result['attributes']:
            if atr.get('objectTypeAttributeId') == 599:
                maint_interval = atr['objectAttributeValues'][0]['displayValue']
                maintinterval = get_date(maint_interval)

                if not maint_hosts.get(maintinterval):
                    maint_hosts[maintinterval] = set()

                maint_hosts[maintinterval].add((host_name, maint_interval))

    print_result(maint_hosts)


if __name__ == '__main__':
    main()
