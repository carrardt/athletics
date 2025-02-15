#!/usr/bin/python3

import time
import sys
import os

# Categories for each birth year
CAT_YEAR = { 2019: 'BB' , 2020: 'BB' , 2016: 'EA' , 2017: 'EA' , 2018: 'EA' , 2014: 'PO' , 2015: 'PO' , 2012: 'BE' , 2013: 'BE' , 2010: 'MI' , 2011: 'MI' }

# first, get that race start time
START_TIME = time.perf_counter()
RACENAME = sys.argv[1]
RUNNERS_FILE = "%s.csv" % RACENAME
RESULT_FILE = "%s-results.csv" % RACENAME
print("Runners <- %s\nResults -> %s"%(RUNNERS_FILE,RESULT_FILE))

# then, we have a little time to initialize everything
BIB_CODE_LEN=13
RUNNERS_LIST=[ [ s.replace('\xa0','').strip() for s in l.split(';') ] for l in open(RUNNERS_FILE).readlines() ]
RUNNERS={}
CATRANK={}
for r in RUNNERS_LIST:
  BIB_CODE=0
  BIB_NUM=0
  try:
    BIB_CODE=int(r[0])
    BIB_NUM=int(r[1])
    YEAR = int(r[4].split('/')[2])
    CATEGORY = CAT_YEAR[YEAR] + r[5]
    RUNNER = [ BIB_NUM , r[2] , r[3] , r[4] , CATEGORY ]
    RUNNERS[ BIB_CODE ] = RUNNER
    CATRANK[RUNNER[4]] = 1
  except:
    print("Skip ",r)

for (k,v) in RUNNERS.items():
    print(k,v)

# in case of failure, we can restart programm
# and get corrzect start time from the first line of results file
START_TIME = time.perf_counter()
rank = 0
try:
    DATA = open(RESULT_FILE,'r').readlines()
    L = DATA[0].split(';')[1].strip().split(':')
    H = int(L[0])
    M = int(L[1])
    S = float(L[2])
    START_TIME = ( H * 3660 ) + ( M * 60 ) + S
    for L in DATA:
      D = L.split(';')
      CAT=D[4].strip()
      if CAT != "":
        CATRANK[CAT] = int(D[5])+1
    rank = int(DATA[-1].split(';')[0])
    print("Restart from %s : T=%.2f , R=%d"%(RESULT_FILE,START_TIME,rank))
    for CAT in CATRANK.keys():
      print("\t%s => %d"%(CAT,CATRANK[CAT]))
except:
    START_TIME = time.perf_counter()
    rank = 0

# print an empty line 
ofile = open(RESULT_FILE,'a+')
SECONDS = time.perf_counter()
MINUTES = int(SECONDS)//60
SECONDS -= MINUTES * 60
HOURS = MINUTES//60
MINUTES -= HOURS*60
output_line = "%04d ; %02d:%02d:%05.2f ; ?%d ; ; ; " % (rank,HOURS,MINUTES,SECONDS,0)
print(output_line)
ofile.write(output_line+'\n')
ofile.flush()
rank = rank + 1

# print human readable start time, not used for actual chrono measure
print("Race start : TIME=%02d:%02d:%05.2f , RANK=%d"%(HOURS,MINUTES,SECONDS,rank) )

BIB_CODE = input()
while BIB_CODE != "end":
    SECONDS = time.perf_counter() - START_TIME
    MINUTES = int(SECONDS)//60
    SECONDS -= MINUTES * 60
    HOURS = MINUTES//60
    MINUTES -= HOURS*60
    BIB_ID=int(BIB_CODE)
    output_line = "";
    CAT = "XX"
    if not BIB_ID in RUNNERS.keys():
        output_line = "%04d ; %02d:%02d:%05.2f ; ?%d ; ; ; " % (rank,HOURS,MINUTES,SECONDS,BIB_ID)
    else:
        runner = RUNNERS[BIB_ID]
        BIB_NUM = runner[0]
        LNAME = runner[1]
        FNAME = runner[2]
        CAT = runner[4]
        crank = CATRANK[CAT]
        output_line = "%05d ; %02d:%02d:%05.2f ; #%05d ; %.20s %.20s ; %s ; %d" % (rank,HOURS,MINUTES,SECONDS,BIB_NUM,LNAME,FNAME,CAT,crank)
        CATRANK[CAT] = CATRANK[CAT] + 1
    print(output_line)
    ofile.write(output_line+'\n')
    ofile.flush()
    rank = rank + 1
    BIB_CODE = input()

