#!/usr/bin/env python3

# cueflac.py
# 24-07-20
# objective:
#   requires templete, joined.cue, joined.flac and cover.jpg
#   extracts tags from template -> tagdict
#   makes the basename: ARTIST - ALBUM, renames/copies files
#   creates mkmeta.sh
#   creates Cuesheet
# returns cuefile name so that it can be checked
# any errors will be handled by sys.exit(1)

import os
import shutil
import sys
from pathlib import Path

from gettagfromtemplate import get_tag_from_template
from makecuesheetheader import make_cuesheet_header
from makecuesheettracks import make_cuesheet_tracks
from makemetafile import make_meta_file


def cueflac():
    # checks for template, joined.cue, joined.flac and cover.jpg
    if not Path("template").exists():
        print('cueflac:"template" file not found', file=sys.stderr)
        sys.exit(1)
    if not Path("filelist").exists():
        print('cueflac:"filelist" file not found', file=sys.stderr)
        sys.exit(1)
    if not Path("joined.cue").exists():
        print('cueflac:"joined.cue" file not found', file=sys.stderr)
        sys.exit(1)
    if not Path("joined.flac").exists():
        print('cueflac:"joined.flac" file not found', file=sys.stderr)
        sys.exit(1)

    # extract tags from template
    tagdict = get_tag_from_template()

    # make the basename: ARTIST - ALBUM
    if tagdict["ALBUMARTIST"]:
        print(f"Multiple artists: |{tagdict['ALBUMARTIST']}|")
        perf = tagdict["ALBUMARTIST"]
    else:
        print("Single artist")
        perf = tagdict["ARTIST"]

    basename = f"{perf} - {tagdict['ALBUM']}"
    print(f"Basename: {basename}")
    flacfile = f"{basename}.flac"
    jpgfile = f"{basename}.jpg"
    cuefile = f"{basename}.cue"

    # check whether files are present
    if not Path("cover.jpg").exists():
        print('cueflac: "cover.jpg" not found, please fix.', file=sys.stderr)
        response = input("Press ENTER when ready to continue : ")
        # check again
        if not Path("cover.jpg").exists():
            print('cueflac: "cover.jpg" not found', file=sys.stderr)
            sys.exit(1)

    # make mkmeta.sh
    make_meta_file(tagdict, basename)

    # make Cuesheet
    header = make_cuesheet_header(tagdict)
    tracks = make_cuesheet_tracks(tagdict)
    try:
        with open(cuefile, "w") as file:
            file.write(header)
            file.write(tracks)
    except OSError as e:
        print(f"cueflac: {e}", file=sys.stderr)
        sys.exit(1)

    print("cueflac completed successfully")
    sys.exit(0)


if __name__ == "__main__":
    cueflac()
