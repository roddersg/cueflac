#!/bin/bash

# blanktemplate24.sh
# 24-07-20
# output is to be re-directed to template file
# if blanktemplate exists, used to create template
# to create a localisted blanktemplate,
#   run blanktemplate24.sh > template
#   edit template
#   rename template to  blanktemplate

if [ -f blanktemplate ]; then
    cat blanktemplate
else
    echo "# blanktemplate--------------------------------------------"
    echo "DISCID="
    echo "ALBUM="
    echo "ALBUMARTIST="
    echo "ARTIST="
    echo "DATE="
    echo "GENRE="
    echo "COMPILATION="
    echo "DISCNUMBER="
    echo "TOTALDISCS="
    echo "COMMENT="$(date +%Y-%m-%d)
fi