#!/bin/bash

# Creates a template file for editing
# 24-07-20
# if template exists, rename to template.old
# if .cue files exist
#     gettagfromcuesheet.py >> template
# blanktemplate.sh >> tempalte
# if template.old
#     cat template.old >> template
# template is ready for editing

# existing template
if [ -f template ]; then
    mv template template.old
fi
# extract from .cue
if ls *.cue 1> /dev/null 2>&1; then
    # echo "Cue files exist"
    for f in *.cue
    do
        echo "# --$f----------" >> template
        ~/python/cueflac/gettagfromcuesheet.py "$f" >> template
    done
else
    echo "No cue files"
fi
# append blank template
source ~/python/cueflac/blanktemplate.sh >> template
# add old template
if [ -f template.old ]; then
    echo "# template.old-------------------------------------------" >> template
    cat template.old >> template
fi

