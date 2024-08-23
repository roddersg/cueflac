#!/usr/bin/env bash

# convert 24/96 or different bit-rates to 16/44 CD quality
# files are kept in 1644 folder

mkdir 1644
for i in *.flac
do
	sox -S "$i" -r 44100 -b 16 1644/"1644_$i"
done

read -p "Make the flac? (Y/n)" mkfl
# default is y
if [ -z $mkfl ] || [ $mkfl == "y" ] || [ $mkfl == "Y" ]
then
    cp template cover.jpg 1644/
    cd 1644
    ~/python/cueflac/mkj24.sh
else
    echo "Conversion complete!"
fi