#!/bin/bash
COUNT=3;
while [ $COUNT -gt 0 ]
do
echo "Process $$ running. Terminates in $COUNT iteration."
sleep 5
COUNT=$(( $COUNT - 1 ))
done
