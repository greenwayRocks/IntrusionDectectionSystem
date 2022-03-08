#!/bin/bash

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
FILENAME='/file.csv'
FILEPATH=$SCRIPTPATH$FILENAME
echo letmein | sudo -S `#to get sudo permissions`\
tshark `#run tshark`\
-T fields -e frame.number -e frame.time -e frame.len -e eth.src -e eth.dst `#give fields to capture`\
-e ip.src -e ip.dst -e ip.proto -e ip.len -e tcp.len -e tcp.srcport -e tcp.dstport -e _ws.col.Info \
-E header=y -E separator="$" -E quote=n -E occurrence=f -a duration:20 `#set headers, separator as comma, double quotations, first occurrence, time`\
> $FILEPATH `#dump into file.csv`\
-i wlan0 `#interface wifi`

# cmd = "echo $password | sudo -S tshark -T fields -e frame.number -e frame.time -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e ip.len -e tcp.len -e tcp.srcport -e tcp.dstport -e _ws.col.Info -E header=y -E separator="$" -E quote=n -E occurrence=f -a duration:20 > $capFile -i $iface"

