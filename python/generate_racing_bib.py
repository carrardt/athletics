#import barcode

FILENAME="/media/carrardt/TC601617/Athle/inscriptions_enfants.csv"
SKIP_LINES=1
FIRST_NAME_FIELD=5
LAST_NAME_FIELD=4
REGISTRATION_ID_FIELD=1
BIRTHDAY_FIELD=17

FIRST_BIB_NUMBER=160
OUTPUT_CSV="bibs.csv"
OUTPUT_PDF="bibs.pdf"

regdatta = [ l.split(';') for l in open(FILENAME).readlines() ]

bib_id = FIRST_BIB_NUMBER
for REG in regdatta[SKIP_LINES:]:
    reg_id = int(REG[REGISTRATION_ID_FIELD-1])
    birthday = REG[BIRTHDAY_FIELD-1].strip()
    last_name = REG[LAST_NAME_FIELD-1].strip('"').strip()
    first_name = REG[FIRST_NAME_FIELD-1].strip('"').strip()
    cat = "CAT"
    print("%04d ; %09d ; % 07s ; % 20s ; % 20s ; % 5s " % (bib_id,reg_id,birthday,last_name,first_name,cat) )
    bib_id = bib_id + 1

