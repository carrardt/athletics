#!/usr/bin/bash

BIBNUM=$1

./mk_range_barcodes.py ${BIBNUM} ${BIBNUM}

convert -background none -density 800 -resize 1000x bib_${BIBNUM}.svg bib_${BIBNUM}.png

convert -size 1600x2262 xc:white \( -size 1400x400 -background white -gravity center -fill black -font "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf" label:"${BIBNUM}" \) -gravity northwest -geometry +250+520 -compose over -composite \( bib_${BIBNUM}.png -resize 800x250! \) -geometry +600+350 -compose over -composite cbib_${BIBNUM}.png

rm -f bib_${BIBNUM}.svg bib_${BIBNUM}.png

