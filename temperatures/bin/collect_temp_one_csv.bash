#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "collect_temp_one_csv <device> <label>"
    exit 1
fi

device=$1
label=$2

DATA=/home/jbf/hapi_home/data/${device}/
DEVICE=/home/jbf/temperatures/sensors/${device}

datetag=`date --utc +%Y%m%d`
year=`date --utc +%Y`

time=`date --utc +%Y-%m-%dT%H:%M:%SZ`

if [ -e $DEVICE ]; then
   # read sensor by cat'ing the file, owfs does this.
   datum=`$DEVICE`
else
   datum=-200;
fi

if [ \! -e ${DATA} ]; then
   mkdir -p ${DATA}
fi

if [ \! -e ${DATA}${year} ]; then
   mkdir -p ${DATA}${year}
fi

datafile=${DATA}${year}/${device}.${datetag}.csv

printf '%s,%s\n' $time $datum >> $datafile

#/home/jbf/eg/owfs/displayotr.py --time=$time --temp=$datum

