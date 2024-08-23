#!/bin/bash

# Moves completed music flac flies to the correct folders
# 28-07-2022
# v 2.0.0

MUSICFOLDER="$HOME/Music/done/cdimages"

echo "Moves completed music files to the Music folder"
echo "Target folder: $MUSICFOLDER"

if [ -z "$1" ]; then
    echo "Usage: $0 <cuefile>"
    exit 1
fi

# check whether files are present
CUEFILE="$1"
FNAME=${CUEFILE:0:-4}
if [ ! -f "$FNAME".cue ] || [ ! -f "$FNAME".flac ] || [ ! -f "$FNAME".jpg ]; then
    echo "Error: File \"$FNAME\" .cue, .flac or .jpg not found in current directory"
    exit 1
fi

# assume no " in the strings
DATE=$(cat "$1" | grep '^REM DATE' | cut -d" " -f3 | tr -d '"')
GENRE=$(cat "$1" | grep '^REM GENRE' | cut -d" " -f3-  | tr -d '"' )
ARTIST=$(cat "$1" | grep "^PERFORMER" | cut -d" " -f2-  | tr -d '"')
ALBUM=$(cat "$1" | grep "^TITLE" | cut -d" " -f2-  | tr -d '"' )

# echo $GENRE
# echo $DATE
# echo $ARTIST
# echo $ALBUM
# echo "-------------------------------"

# basename for files
BASENAME="$ARTIST - $ALBUM"

# fix any "The <artist>" to "<artist>, The"
ARTIST=$(echo "$ARTIST" | sed 's|^The \(.*\)|\1, The|')
# remove any CDxx ... from album
ALBUMDIR=$(echo $ALBUM | sed 's| CD[0-9][0-9].*$||;s|[[:space:]]$||')

TARGETDIR="$MUSICFOLDER"
if [[ "$GENRE" == "Soundtrack" ]] || [[ "$GENRE" == "Christmas" ]]; then
    TARGETDIR="$TARGETDIR/$GENRE"
fi
TARGETDIR="$TARGETDIR/$ARTIST/$DATE-$ALBUMDIR/"

echo "TARGET="$TARGETDIR
echo "Files: ${BASENAME} .cue, .flac, .jpg"

read -p "Move the files? (Y/n) : " response
response=$(echo $response | tr '[:upper:]' '[:lower:]')
if [[ -z $response ]] || [[ $response == "y" ]] ; then
    mkdir -p "$TARGETDIR"
    mv "${BASENAME}.jpg" "${BASENAME}.flac" "${BASENAME}.cue" "$TARGETDIR"
    echo "Done!"
else
    echo "Aborted!"
    exit 1
fi
