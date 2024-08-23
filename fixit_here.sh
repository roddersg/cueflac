
#!/bin/bash

echo "fixit_here.sh"

# does fixit in the local folder, does not move the files, cleans up

# ASSUMES FILENAME.cue exists and is CORRECT
# ONLY changes the tags in the .flac file
    # extracts template from FILENAME.cue
    # regenerates BASENAME using template
    # if cover.jpg does not exist,
        # renames FILENAME.jpg to cover.jpg
    # renames FILENAME.flac to joined.flac
    # does cueflac.py but does not call shntool cue, shntool join
        # creates mkmeta.sh
        # executes mkmeta.sh
    # renames cover.jpg to FILENAME.jpg
    # renames joined.flac to FILENAME.flac
    # moves FILENAME(cue,flac,jpg) to Music folder
    # does cleanup
#
# must have FILENAME argument with .cue extension
if [ -z "$1" ]; then
    echo "Usage: fixit24.sh FILENAME.cue"
    exit 1
fi
filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"
echo "Filename: [$filename]  Extension: [$extension]"
if [ $extension != "cue" ]; then
    echo "Usage: fixit24.sh FILENAME.cue"
    exit 1
fi
# extract the tags
~/python/cueflac/gettagfromcuesheet.py "$1" > template
# rename the flac and jpg
mv -vv "${filename}".flac joined.flac
if [ ! -f cover.jpg ]; then
    mv -vv "${filename}".jpg cover.jpg
fi
# prepare the mkmeta.sh
~/python/cueflac/makemetafilefromcuesheet.py "$1"

# when ready to proceed press enter
# read -p "Ready to execute mkmeta.sh ? (Y/n) : " response
# response=$(echo "$response" | tr '[:upper:]' '[:lower:]')
# if [ -z "$response" ] || [ "$response" = "y" ]; then
# # read -p "Do you want to continue? (Y/n) : " response
# # # Check the response
# # if [ -z "$response" ] || [[ "$response" =~ ^[Yy]$ ]] ; then
# # write in the tags
#     CURRENT_DIR=$(pwd)
#     echo "${CURRENT_DIR}/mkmeta.sh"
#     . "${CURRENT_DIR}/"mkmeta.sh
#     # source ./mkmeta.sh
#     if [ "$?" -ne 0 ]; then
#     	echo "Failure: problems with mkmeta.sh"
#         exit 1
#     fi
# else
#     exit 2
# fi
CURRENT_DIR=$(pwd)
echo "${CURRENT_DIR}/mkmeta.sh"
. "${CURRENT_DIR}/"mkmeta.sh
# source ./mkmeta.sh
if [ "$?" -ne 0 ]; then
    echo "Failure: problems with mkmeta.sh"
    exit 1
fi


# move the files
# ~/python/cueflac/movemusic.sh "${filename}.cue"

# cleanup
# read -p "Cleanup folder (remove mkmeta, cover, template) ? (Y/n) : " response
# response=$(echo "$response" | tr '[:upper:]' '[:lower:]')
# if [ -z "$response" ] || [ "$response" = "y" ]; then
#     \rm mkmeta.sh cover.jpg template
# fi
\rm mkmeta.sh cover.jpg template

# let's do a flac check
filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"
flacfile="${filename}.flac"
~/python/cueflac/flacinfo.py "$flacfile"
