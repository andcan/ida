#!/bin/bash

dir='data'

count=1
while [ $count -gt 0 ]; do
   count=`find "$dir" -type f \( -iname '*.zip' -o -iname '*.rar' \) -exec ./unpacker.sh \{\} \; | wc -l`
done
