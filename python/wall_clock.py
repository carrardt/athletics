#!/usr/bin/python3

import time

T0 = time.perf_counter()
print("=== CHRONO ===")
while True:
    SECONDS=time.perf_counter()-T0
    MINUTES = int(SECONDS)//60
    SECONDS -= MINUTES*60
    HOURS = MINUTES//60
    MINUTES -= HOURS*60
    print("%02d:%02d:%02.2f          \r"%(HOURS,MINUTES,SECONDS),end="")
    time.sleep(1)

