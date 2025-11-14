"""
    File: deletion_timer.py
    Version: 12 November 2025
    Author: James Tedder
    Description:
        A shell for a timer that will trigger the daily
        deletion task that will be made in part 3. 
        Currently does nothing.
        It will run the deletion task immediately when 
        it is ran and then when it is a new day. It will check 
        every minute after it is ran.
        Sched should be compatible with multiple threads but if 
        there are issues this may be a good place to look.
"""

import sched
import time

last_deletion = time.gmtime(0)
s = sched.scheduler(time.time, time.sleep)
def check_time ():
    global last_deletion
    if (last_deletion.tm_mday != time.localtime().tm_mday):
        #TODO: add deletion call
        last_deletion = time.localtime()

check_time()
while(True):
    s.enter(60,1,check_time)
    s.run()