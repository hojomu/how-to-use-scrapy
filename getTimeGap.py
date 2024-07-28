from datetime import datetime
from dateutil.relativedelta import relativedelta

# 주어진 시간
given_time = datetime.strptime('1970/01/20 08:48', '%Y/%m/%d %H:%M')

# 현재 시간
current_time = datetime.now()

# 시간 차이 계산
difference = relativedelta(current_time, given_time)

# 차이 출력
print(f"Difference is {difference.years} years, {difference.months} months, {difference.days} days, "
      f"{difference.hours} hours, and {difference.minutes} minutes.")