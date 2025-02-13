#!/usr/bin/python3

import time
import sys

# Categories for each birth year
CAT_YEAR = { 2019: 'BB' , 2020: 'BB' , 2016: 'EA' , 2017: 'EA' , 2018: 'EA' , 2014: 'PO' , 2015: 'PO' , 2012: 'BE' , 2013: 'BE' , 2010: 'MI' , 2011: 'MI' }

# first, get that race start time
START_TIME = time.perf_counter()
RUNNERS_FILE = sys.argv[1]
RESULT_FILE = sys.argv[2]
print("Runners <- %s\nResults -> %s"%(RUNNERS_FILE,RESULT_FILE))

# then, we have a little time to initialize everything
BIB_CODE_LEN=13
RUNNERS_LIST=[ [ s.strip() for s in l.split(';') ] for l in open(RUNNERS_FILE).readlines() ]
RUNNERS={}
CATRANK={}
for r in RUNNERS_LIST:
    RUNNERS[ int(r[0]) ] = r
    CATRANK[r[5]] = 1

for (k,v) in RUNNERS.items():
    print(k,v)

ofile = open(RESULT_FILE,'a+')

# print human readable start time, not used for actual chrono measure
tod = time.localtime()
print("Race started at %02dh %02dm %02ds"%(tod.tm_hour,tod.tm_min,tod.tm_sec))
START_TIME = time.perf_counter()

rank=1
BIB_CODE = input()
while BIB_CODE != "end":
    SECONDS = time.perf_counter() - START_TIME
    MINUTES = int(SECONDS)//60
    SECONDS -= MINUTES * 60
    HOURS = MINUTES//60
    MINUTES -= HOURS*60
    BIB_ID=int(BIB_CODE)
    output_line = "";
    if not BIB_ID in RUNNERS.keys():
        output_line = "%04d ; %02d:%02d:%05.2f ; ?%d ; ; ; " % (rank,HOURS,MINUTES,SECONDS,BIB_ID)
    else:
        runner = RUNNERS[BIB_ID]
        crank = CATRANK[runner[5]]
        output_line = "%04d ; %02d:%02d:%05.2f ; #%.13s ; %.20s %.20s ; %s ; %d" % (rank,HOURS,MINUTES,SECONDS,runner[1],runner[3],runner[4],runner[5],crank)
    print(output_line)
    ofile.write(output_line+'\n')
    ofile.flush()
    rank = rank + 1
    CATRANK[runner[5]] = crank + 1
    BIB_CODE = input()

