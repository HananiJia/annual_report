import os
CSV_PATH = 'yihang.csv'
LINES = 1000
SEND_COUNT = 0
RECEIVE_COUNT = 0


if __name__ == '__main__':
    f= open (CSV_PATH,'r')
    index = 0
    for r in f.readlines():
        if '已接收' in r:
            RECEIVE_COUNT += 1
        elif '已发送' in r:
            SEND_COUNT += 1
        else:
            print(r)
    print(f'send message {SEND_COUNT}')
    print(f'recevie message {RECEIVE_COUNT}')