#!/usr/bin/bash

RACENAME="Cource1K"

xterm -T "${RACENAME}" -geometry 20x2+0+0 -fa 'Monospace' -fs 32 -e "./wall_clock.py" &

wait
echo "Finished"
