#!/bin/bash

# establish music dir
MUSICFOLDER="$HOME/Music/done/cdimages/"

echo "mkj24"
echo "-----------------------------------------------------------"

echo "removing joined.* filelist* mkmeta.sh"
rm joined.* filelist.* mkmeta.sh

# make template
source ~/python/cueflac/maketemplate.sh


# generate list of .flac files for processing
#--------------------
#  ${parameter:-word} If parameter is unset or null, the expansion of word is
#  substituted. Otherwise, the value of parameter is substituted.
# read -p "Does album have MULTIPLE artists [y/N] : " ans
# ans = ${ans:-N)
#-------------------
#  This option requires bash 4 or higher (bash --version)
#  On macos, install current bash using homebrew - brew.sh
#  -e and -i work together:
#    -e uses readline,
#    -i inserts text using readline
#  displays the default value at the prompt
read -p "Does album have MULTIPLE artists (y/N) : " response
response=$(echo "$response" | tr '[:upper:]' '[:lower:]')
if [ -z "$response" ] || [[ "$response" == "n" ]]; then
	MULTIPLE=""
else
    MULTIPLE="-m"
fi

# create the files to join
~/python/cueflac/cleanfilelist.py $MULTIPLE

# allow user to change template and filelist and see any .nfo files
subl template filelist

# in the meantime, make joined.cue and joined.flac
shntool cue -F filelist.org > joined.cue
if [[ $? != 0 ]]; then
	echo "shntool cue: Error, cannot create joined.cue"
	exit 2
fi
shntool join -F filelist.org -o flac
if [[ $? != 0 ]]; then
	echo "shntool join: Error, cannot create joined.flac"
	exit 2
fi

# when ready to proceed press enter
read -p "Finished join, press ENTER when ready to run cueflac.py : " response
# use cueflac.py to generate the ./mkmeta file
~/python/cueflac/cueflac.py
status=$?
if [[ $status != 0 ]]; then
	echo "cueflac failed."
	exit 1
fi

ARTIST=$( ~/python/cueflac/gettagfromtemplate.py -t "artist")
ALBUM=$( ~/python/cueflac/gettagfromtemplate.py -t "album")
YEAR=$( ~/python/cueflac/gettagfromtemplate.py -t "date")
GENRE=$( ~/python/cueflac/gettagfromtemplate.py -t "genre")
BASENAME="$ARTIST - $ALBUM"

# need to check Cuesheet before inserting tags
subl "${BASENAME}.cue"

# when ready to proceed press enter
read -p "check CUESHEET, press ENTER when ready to continue : " response
# write in the tags
CURRENT_DIR=$(pwd)
source "${CURRENT_DIR}/mkmeta.sh"
if [[ "$?" != 0 ]]; then
	echo "Failure: problems with mkmeta.sh"
fi

# move the files
~/python/cueflac/movemusic.sh "${BASENAME}.cue"