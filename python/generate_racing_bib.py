import os
import barcode

# to convert output SVGs to multipage pdf, use the following command :
# convert -density 300 *.svg output.pdf

FILENAME=os.getenv('HOME')+"/inscriptions_enfants.csv"
SKIP_LINES=1
FIRST_NAME_FIELD=5
LAST_NAME_FIELD=4
REGISTRATION_ID_FIELD=1
RACE_NAME_FIELD=13
BIRTHDAY_FIELD=17

FIRST_BIB_NUMBER=160
OUTPUT_CSV="bibs.csv"
OUTPUT_SVG="bib_%04d.svg"

RACE_NAME_LEN=11
RACE_IDS = { "course 1km ": 1 , "course 2 km": 2 }

CAT_YEAR = { 2019: 'BB' , 2020: 'BB' , 2016: 'EA' , 2017: 'EA' , 2018: 'EA' , 2014: 'PO' , 2015: 'PO' , 2012: 'BE' , 2013: 'BE' , 2010: 'MI' , 2011: 'MI' }

regdatta = [ l.split(';') for l in open(FILENAME).readlines() ]

bib_csv = open(OUTPUT_CSV,'w')
bib_id = FIRST_BIB_NUMBER
for REG in regdatta[SKIP_LINES:]:
    reg_id = int(REG[REGISTRATION_ID_FIELD-1])
    birthday = REG[BIRTHDAY_FIELD-1].strip()
    year = int(birthday.split('/')[-1])
    print("bday='%s' , year=%d"%(birthday,year))
    last_name = REG[LAST_NAME_FIELD-1].strip('"').strip()
    first_name = REG[FIRST_NAME_FIELD-1].strip('"').strip()
    race_id = RACE_IDS[ REG[RACE_NAME_FIELD-1][:RACE_NAME_LEN] ]
    if not year in CAT_YEAR.keys():
        print("year %d not in CAT_YEAR"%year)
    cat = CAT_YEAR[year] + "x"
    bib_csv.write( "%04d ; %09d ; % 07s ; % 20s ; % 20s ; % 5s\n" % (bib_id,reg_id,birthday,last_name,first_name,cat) )
    barcode_data = "%04d%04d%04d" % (bib_id,year,race_id)
    print(barcode_data)
    barcode.EAN13(barcode_data,writer=barcode.writer.SVGWriter()).write(open(OUTPUT_SVG%bib_id,'wb'))
    bib_id = bib_id + 1

