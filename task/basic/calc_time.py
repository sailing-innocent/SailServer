# -*- coding: utf-8 -*-
# @file demo.py
# @brief The Demo
# @author sailing-innocent
# @date 2025-02-19
# @version 1.0
# ---------------------------------

from datetime import datetime 
from datetime import timedelta

PROJECT_START_TIMESTAMP = 0 # 1970-01-01 00:00:00
PROJECT_END_TIMESTAMP = 4733481600 # 2120-01-01 00:00:00
BASIC_TIME_TICK = 20 * 60 # 20 minutes

if __name__ == "__main__":
    today = datetime.today()
    print(int(today.timestamp()))
    # the date 100 days after
    print(today + timedelta(days=100))
    # the date 74 years after
    print(today + timedelta(days=74*365))
    # 2120年1月1日
    PROJECT_END_DATE = datetime(2120, 1, 1)
    timpstamp = PROJECT_END_DATE.timestamp()
    print(timpstamp)
    N_ticks = int((timpstamp - PROJECT_START_TIMESTAMP) / BASIC_TIME_TICK)
    print(N_ticks)
    ALIVE_START_DATE = datetime(1999, 4, 19)
    ALIVE_END_DATE = datetime(2100, 1,1)
    ALIVE_START_TIMESTAMP = ALIVE_START_DATE.timestamp()
    ALIVE_END_TIMESTAMP = ALIVE_END_DATE.timestamp()
    print(ALIVE_START_TIMESTAMP)
    print(ALIVE_END_TIMESTAMP)

    print(int((ALIVE_END_TIMESTAMP - ALIVE_START_TIMESTAMP) / BASIC_TIME_TICK))
    now = datetime.now()
    NOW_TIMESTAMP = now.timestamp()
    print(NOW_TIMESTAMP)
    print(int((NOW_TIMESTAMP - ALIVE_START_TIMESTAMP) / BASIC_TIME_TICK))
    print(int((ALIVE_END_TIMESTAMP - NOW_TIMESTAMP) / BASIC_TIME_TICK))
