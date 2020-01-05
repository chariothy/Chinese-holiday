 #!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   parse_holiday.py
@Time    :   2019/12/26 09:21:37
@Author  :   Chariothy 
@Version :   1.0
@Contact :   chariothy@gmail.com
@Desc    :   从国务院官网解析节假日信息
'''

import requests
from bs4 import BeautifulSoup
import re, os, json
import datetime as dt
from datetime import datetime
import time
from urllib import parse

HOLIDAY_DATA_PATH = os.path.join(os.getcwd(), 'holiday.json')


def get_holiday_data(year, force_refresh=False):
    """加载节假日数据，没有则去国务院网站解析
    
    Keyword Arguments:
        year {str} -- 四位数字年份
        force_refresh {bool} -- 是否强制加载 (default: {False})
    
    Returns:
        array -- 节假日数组，每行格式为：(from_date, to_date, need_work)
                 如： ('2020-1-1', '2020-1-1', False) 表示2020-1-1放假
                     ('2020-10-1', '2020-10-8', False) 表示2020-10-1到2020-10-8放假
                     ('2020-1-19', '2020-1-19', True) 表示2020-1-19补班
    """
    year = str(year)
    all_holiday = {}
    holiday_data = None
    if os.path.exists(HOLIDAY_DATA_PATH):
        with open(HOLIDAY_DATA_PATH, 'r', encoding='utf8') as fp:
            try:
                all_holiday = json.load(fp)
            except Exception:
                all_holiday = {}
            if type(all_holiday) == dict:
                holiday_data = all_holiday.get(str(year), None)
    if holiday_data is None or force_refresh:
        url = search_notice_url(year)
        parsed_year, holiday_data = parse_holiday_info(url)
        if parsed_year != year or len(holiday_data) == 0:
            raise Exception('Can not parse holiday info from {}.'.format(url))
        all_holiday[year] = holiday_data
        with open(HOLIDAY_DATA_PATH, 'w', encoding='utf8') as fp:
            json.dump(all_holiday, fp, indent=2, ensure_ascii=False)
    return holiday_data


def is_holiday(date_time):
    """判断日期是否是节假日（包含正常周末和法定节假日）
    
    Arguments:
        date_time {str} -- 日期，格式: yyyy-mm-dd
    
    Returns:
        bool -- 是否为假日
    """
    if type(date_time) == str:
        date_time = datetime.strptime(date_time, '%Y-%m-%d')
    assert type(date_time) == datetime

    year = date_time.strftime('%Y')
    holiday_lines = get_holiday_data(year)
    assert type(holiday_lines) == list and len(holiday_lines) > 0
    for holiday_line in holiday_lines:
        from_date, to_date, work = holiday_line
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
        if date_time >= from_date and date_time <= to_date:
            return not work
    if date_time.weekday() in (5, 6):
        return True
    else:
        return False
    return True


def search_notice_url(year):
    """从国务院网站查询节假日公告链接
    Arguments:
        year {str} -- 四位数字的年份
    Returns:
        str -- 公告链接
    Raises:
        Exception: 解析搜索结果出错
    """
    title = '国务院办公厅关于{}年部分节假日安排的通知'.format(year)

    param = {
        't': 'bulletin',
        'advance': 'true',
        'sug_t': 'bulletin',
        'sug_size': 5,
        'pubcpnSel': '国务院办公厅',
        'pubtypeSel': '国办发明电',
        'timetype': 'timezd',
        'contenttype': '综合',
        'title': title 
    }

    url = 'http://sousuo.gov.cn/s.htm?' + parse.urlencode(param)
    #print(url)
    response = requests.get(url)
    page_content = decode_response_content(response).decode('utf8')
    #print(page_content)
    
    soup = BeautifulSoup(page_content, features="html.parser")
    try:
        hrefs = soup.find('div', class_='result').find_all('a')
        for href in hrefs:
            if href.get_text() == title:
                return href['href']
    except Exception as ex:
        raise Exception('Failure to search link {} from {}. Inner exception: {}'.format(title, url, ex))
    return None


def decode_response_content(response):
    """当无法从网页预测出编码格式时，为网页内容解码
    
    Arguments:
        response {} -- 网页响应
    
    Returns:
        str -- 解码后的内容
    """
    page_content = response.content
    if response.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(response.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = response.apparent_encoding
        page_content = response.content.decode(encoding, 'replace') #如果设置为replace，则会用?取代非法字符；
    return page_content


def parse_holiday_info(url):
    """从国务院公告链接中解析节假日信息
    
    Arguments:
        url {str} -- 国务院节假日公告链接
    
    Raises:
        Exception: 公告内容非预期
    """
    session = requests.Session()
    response = session.get(url, stream=True)
    page_content = decode_response_content(response)
    soup = BeautifulSoup(page_content, features="html.parser")
    text = soup.find(id='UCAP-CONTENT').get_text()
    #print(text)
    
    holiday_lines = text.split()
    holiday_data = []
    year = ''

    for holiday_line in holiday_lines:
        match = re.match(r'国务院办公厅关于(\d{4})年', holiday_line)
        if match:
            year = match.group(1)
            break
    if len(year) == 0:
        raise Exception('Wrong message: ' + text)
    
    reg_holiday_occur = re.compile(r'''
((?:\d{4}年)?\d{1,2}月\d{1,2}日)                #开始日
(?:至((?:\d{4}年)?(?:\d{1,2}月)?\d{1,2}日))?    #结束日，可能没有
放假.*?
(?:共(\d)天)?。                                 #天数，可能没有
''', re.VERBOSE
    )
    for holiday_line in holiday_lines:
        holiday_occur = reg_holiday_occur.search(holiday_line)
        if holiday_occur:
            first_holiday, last_holiday, count_day = holiday_occur.groups()
            if count_day is None:
                #TODO: 未来可能公告中不出现“共3天”，届时从last_holiday推算
                count_day = '1'
            if '年' not in first_holiday:
                first_holiday = year + '年' + first_holiday

            #print(first_holiday, last_holiday, count)
            first_holiday = datetime.strptime(first_holiday, '%Y年%m月%d日')
            last_holiday = first_holiday + dt.timedelta(days = int(count_day)-1)
            holiday_data.append((first_holiday.strftime("%Y-%m-%d"), last_holiday.strftime("%Y-%m-%d"), False))

        workday_occur = re.search(r'((?:(?:\d{4}年)?\d{1,2}月\d{1,2}日（星期.+?）、?)+)上班。', holiday_line)
        if workday_occur:
            work_str = workday_occur.group(1)
            workdays = re.findall(r'(?:\d{4}年)?\d{1,2}月\d{1,2}日', work_str)
            for workday in workdays:
                if '年' not in workday:
                    workday = year + '年' + workday
                workday = datetime.strptime(workday, '%Y年%m月%d日').strftime("%Y-%m-%d")
                holiday_data.append((workday, workday, True))
    #print('-'*100)
    #print(year, holiday_data)
    return (year, holiday_data)



if __name__ == "__main__":
    #notice_url = search_notice_url(2020)
    #holiday = parse_holiday_info(notice_url)
    print(is_holiday('2019-10-10'))