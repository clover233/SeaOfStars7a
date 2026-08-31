#!/bin/bash
i=1
while ((i <= 6000))
do
    ((i++))
    cat /sys/class/ithermal/lpm/lpm_freq >> /data/local/tmp/ddr_info.txt
    sleep 3
done
