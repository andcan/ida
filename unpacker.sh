#!/bin/bash
basename=`basename "$1"`
basedir=`dirname "$1"`

cd "$basedir"
ext=`echo "$basename" | awk -F . '{print $NF}'`

if [ "$ext" = "zip" ]; then
  basenamenoext="${basename/.zip/}"
  mkdir -p "$basenamenoext"
  7z x -pandrea -o"$basenamenoext" "$basename"
  if [ $? -eq 0 ]; then
     echo "zip unpacked: $1"
     rm "$basename"
  fi
fi

if [ "$ext" = "rar" ]; then
  basenamenoext="${basename/.rar/}"
  mkdir -p "$basenamenoext"
  mv "$basename" "$basenamenoext"
  cd "$basenamenoext"
  unrar e -pandrea -y -c- -inul "$basename"
  if [ $? -eq 0 ]; then
     echo "rar unpacked: $1"
     rm "$basename"
  fi
fi