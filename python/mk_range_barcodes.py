#!/usr/bin/python3

import os
import barcode

OUTPUT_SVG="bib_%04d.svg"

for i in range(260,360):
    barcode_data = "%012d" % i
    print(barcode_data)
    barcode.EAN13(barcode_data,writer=barcode.writer.SVGWriter()).write(open(OUTPUT_SVG%i,'wb'))

