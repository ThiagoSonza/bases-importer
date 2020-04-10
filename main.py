#!/usr/bin/python3
import time
import datetime
import schedule
from principal import principal

def job():
    principal.main()


schedule.every(1).days.at("19:00").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)