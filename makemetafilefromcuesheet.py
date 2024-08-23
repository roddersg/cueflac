#!/usr/bin/env python3

# makemetafilefromcuesheet.py
# 24-07-20
# function: makeMetaFile
# creates a meta file
# if executed as a program it prints the meta file which can be re-directed to a file
# uses make_meta_file(), get_tag_from_cuesheet()

import sys

import click

from gettagfromcuesheet import get_tag_from_cuesheet
from makemetafile import make_meta_file


@click.command()
@click.argument("filename", type=click.Path(exists=True, file_okay=True, dir_okay=False))
def cli(filename):
    """
    Creates mkmeta.sh from cuesheet

    FILENAME - a path to a cuesheet (required).
    """
    if filename.endswith(".cue"):
        tagdict = get_tag_from_cuesheet(filename)
        basename = filename[:-4]
    else:
        print(f"{filename} is not a cuesheet", file=sys.stderr)
        sys.exit(1)

    make_meta_file(tagdict, basename)


if __name__ == "__main__":
    cli()
