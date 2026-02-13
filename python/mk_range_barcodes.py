#!/usr/bin/python3

import os
import barcode
import sys

BS=int(sys.argv[1])
BE=int(sys.argv[2])+1

OUTPUT_SVG="bib_%04d.svg"

for i in range(BS,BE):
    barcode_data = "%012d" % i
    print(barcode_data)
    barcode.EAN13(barcode_data,writer=barcode.writer.SVGWriter()).write(open(OUTPUT_SVG%i,'wb'))

