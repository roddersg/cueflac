#!/usr/bin/env python3

# makeMetaFile.py
# 24-07-20
# function: makeMetaFile
# creates a meta file
# if executed as a program it prints the meta file which can be re-directed to a file

import os
import stat
import sys


def make_meta_file(tagdict: dict, basename: str):
    """
    makes the meta file from the tagdict - mkmeta.sh
    """

    flacfile = f"{basename}.flac"
    jpgfile = f"{basename}.jpg"
    cuefile = f"{basename}.cue"
    try:
        with open("mkmeta.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f'mv -vv joined.flac "{flacfile}"\n')
            f.write(f'cp -vv cover.jpg "{jpgfile}"\n')
            f.write(f'metaflac --remove-all "{flacfile}"\n')
            f.write("metaflac ")
            for tag in tagdict:
                f.write(f' --set-tag={tag}="{tagdict[tag]}"')
            f.write(f' --set-tag-from-file=CUESHEET="{cuefile}"')
            f.write(f' --import-cuesheet-from="{cuefile}"')
            f.write(f' --import-picture-from="{jpgfile}"')
            f.write(f' "{flacfile}"\n')
        os.chmod("mkmeta.sh", stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    except OSError as e:
        print(f"makeMetaFile: {e}")
        sys.exit(2)
    print("mkmeta.sh created successfully")
    return


if __name__ == "__main__":

    from gettagfromtemplate import get_tag_from_template

    tagdict = get_tag_from_template()
    make_meta_file(tagdict)
