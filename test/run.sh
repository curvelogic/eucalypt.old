#!/bin/bash

OUTPUTDIR=./out
mkdir -p $OUTPUTDIR


test() {
    script=$1

    echo "*** Running $script ***"
    "./$script" > $OUTPUTDIR/${script%.eu}.out.txt

    if [ $? -eq 0 ] ; then
	echo "*** SUCCESS ***"
    else
	echo "*** FAILURE ***"
    fi
}

for f in *.eu; do
    test $f
done
