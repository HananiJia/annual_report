import datetime

today = datetime.datetime.now().weekday() + 1
print(today)

week = datetime.datetime.strptime("20201231", "%Y%m%d").weekday() + 1
print(week)