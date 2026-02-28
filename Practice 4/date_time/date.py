#1:
from datetime import datetime, timedelta
today = datetime.now()
new = today- timedelta(days=5)
print(new)
#2:
today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
#3:
today = datetime.now().replace(microsecond=0)
print(today)
#4:
d1 = input()
d2 = input()
date_format = "%Y-%m-%d %H:%M:%S"
date1 = datetime.strptime(d1, date_format)
date2 = datetime.strptime(d2, date_format)
difference = abs((date2 - date1).total_seconds())
print(int(difference))