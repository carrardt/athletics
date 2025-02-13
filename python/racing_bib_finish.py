#!/usr/bin/python3

import time
import sys

# first, get that race start time
START_TIME = time.perf_counter()
RUNNERS_FILE = sys.argv[1]
RESULT_FILE = sys.argv[2]
print("read runners from %s, write results to %s"%(RUNNERS_FILE,RESULT_FILE))

# then, we have a little time to initialize everything
BIB_CODE_LEN=13
RUNNERS_LIST=[ [ s.strip() for s in l.split(';') ] for l in open(RUNNERS_FILE).readlines() ]
RUNNERS={}
CATRANK={}
for r in RUNNERS_LIST:
    RUNNERS[ int(r[0]) ] = r
    CATRANK[r[5]] = 1
print(RUNNERS)

ofile = open(RESULT_FILE,'a+')

# print human readable start time, not used for actual chrono measure
tod = time.localtime()
print("Race started at %02dh %02dm %02ds"%(tod.tm_hour,tod.tm_min,tod.tm_sec))
START_TIME = time.perf_counter()

rank=1
BIB_CODE = input()
while BIB_CODE != "end":
    ELAPSED = time.perf_counter() - START_TIME
    BIB_ID=int(BIB_CODE)
    if not BIB_ID in RUNNERS.keys():
        print("---- : #%04d not in base"%BIB_ID)
    else:
        runner = RUNNERS[BIB_ID]
        crank = CATRANK[runner[5]]
        output_line = "%04d ; %05.2f ; #%04d ; %.20s %.20s ; %s ; %d" % (rank,ELAPSED,BIB_ID,runner[3],runner[4],runner[5],crank)
        print(output_line)
        ofile.write(output_line+'\n')
        rank = rank + 1
        CATRANK[runner[5]] = crank + 1
    BIB_CODE = input()

