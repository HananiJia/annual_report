import os
import re
import json
import jieba
import jieba.analyse
import time, datetime
from collections import defaultdict

CSV_PATH = 'yihang.csv'
JSON_PATH = 'report.json'
pattern = re.compile("^[0-9a-z]+$")
data_format = "%Y/%m/%d %H:%M"
DELETE_KEYS = [' ', '我', '了', '你', '的']


def analysis(msg_list):
    print('start')
    most_num = -1
    least_num = -1
    day = ''
    month = defaultdict(int)
    hour = defaultdict(int)
    cut_content = defaultdict(int)
    msg_count = 0
    pictures = 0
    videos = 0
    calls = 0
    emoticons = 0
    call_hour = 0
    call_min = 0
    call_sec = 0
    day_messages = {}
    all_msgs = ''
    analysis_json = {'total': len(msg_list), 'most': {}, 'least': {}}
    for msgs in msg_list:
        tags = msgs[0].split(',')
        date = datetime.datetime.strptime(tags[2], data_format)
        today = date.strftime('%Y/%m/%d')
        month[date.month] += 1
        hour[date.hour] += 1
        # if date.hour <= 6 and date.hour >= 4:
        #     print(tags[2])
        #     print(msgs[1])
        if day == '':
            day = today
            msg_count += 1
        if today == day:
            msg_count += 1
        else:
            day_messages[day] = msg_count
            if msg_count > most_num:
                most_num = msg_count
                analysis_json['most']['day'] = day
                analysis_json['most']['num'] = most_num
            if least_num == -1 or msg_count < least_num:
                least_num = msg_count
                analysis_json['least']['day'] = day
                analysis_json['least']['num'] = least_num
            msg_count = 1
            day = today
        msg = msgs[1].strip()
        if 'wx_emoji' in msg or (pattern.match(msg) and len(msg) == 32) or (
                'http://vweixinf.tc.qq.com' in msg):
            emoticons += 1
        elif '<AUNBOX TYPE=""7"">' in msg:
            pass
        elif 'http' in msg:
            pass
        elif 'E:\ifonebackup\Versions' in msg:
            pictures += 1
        elif '.wav' in msg:
            videos += 1
        elif '通话时长 ' in msg:
            calls += 1
            msg = msg[msg.index(' ') + 1:]
            call_time = msg.split(':')
            if len(call_time) == 3:
                call_hour += int(call_time[0])
            call_min += int(call_time[-2])
            call_sec += int(call_time[-1])
        else:
            all_msgs += msgs[1]
            cut_msg = jieba.cut(msgs[1].strip())
            # print(msg)
            # print(cut_msg)
            for m in cut_msg:
                if len(m) == 1:
                    continue
                if m in DELETE_KEYS:
                    continue
                cut_content[m] += 1
    cut_content = sorted(cut_content.items(), key=lambda d: d[1], reverse=True)
    print(json.dumps(cut_content, indent=4, ensure_ascii=False))
    keywords = jieba.analyse.extract_tags(all_msgs, topK=50, withWeight=True)
    for k in keywords:
        print(k[0], k[1])
    call_min += int(call_sec / 60)
    call_sec = call_sec % 60
    call_hour += int(call_min / 60)
    call_min = call_min % 60
    analysis_json['emoticons'] = emoticons
    analysis_json['pictures'] = pictures
    analysis_json['videos'] = videos
    analysis_json['calls'] = {
        '#calls': calls,
        'hours': call_hour,
        'minute': call_min,
        'second': call_sec
    }
    analysis_json['day2msg'] = day_messages
    analysis_json['month'] = month
    analysis_json['hour'] = hour
    return analysis_json


if __name__ == '__main__':
    f = open(CSV_PATH, 'r')
    send_list = []
    receive_list = []
    for r in f.readlines():
        if '已接收' in r:
            receive_list.append(r.split('已接收,'))
        elif '已发送' in r:
            send_list.append(r.split('已发送,'))
    f.close()
    msg_json = {'time': time.time()}
    msg_json['receive'] = analysis(receive_list)
    msg_json['send'] = analysis(send_list)
    # print(json.dumps(msg_json, indent=4))
    with open(JSON_PATH, 'w') as f:
        json.dump(msg_json, f, indent=4)
