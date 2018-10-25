from datetime import datetime

speed = '1:11.40'
zero = '0:00.00'
zero = datetime.strptime(zero, '%M:%S.%f')
if len(speed) > 5:
    new = datetime.strptime(speed, '%M:%S.%f')
else:
    new = datetime.strptime(speed, '%S.%f')
print((new-zero).total_seconds())

date = 'January 6, 2018'
date = datetime.strptime(date, '%b %d, %Y').date()
print(date)
