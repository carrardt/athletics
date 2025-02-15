#!/usr/bin/bash

RACENAME="$1"

xterm -T "${RACENAME} CHRONO" -geometry 20x2+0+0 -fa 'Monospace' -fs 32 -e "./wall_clock.py" &
xterm -T "${RACENAME} FINISH" -geometry 100x30+0+180 -fa 'Monospace' -fs 18 -e "./racing_bib_finish.py ${RACENAME}"

wait
echo "Finished"
