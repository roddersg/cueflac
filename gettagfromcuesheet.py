#!/usr/bin/env python3

# gettagfromcuesheet.py
# 24-07-20
# returns a dictionary of tags from a cuesheet

import sys
from datetime import date
from pathlib import Path

import click


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: word.group(0).capitalize(), s)


def dequote(s: str) -> str:
    """
    removes spaces, quotes, double-quotes from string
    """
    s = s.strip()
    if len(s) > 2 and s[0] == s[-1] and s.startswith(('"', "'")):
        return s[1:-1]
    return s


def get_tag_from_cuesheet(cuesheetfile: str) -> dict:
    """
    returns a dictionary of the tags from the cuesheet
    """
    tagdict = {
        "DISCID": "",
        "ARTIST": "",
        "ALBUM": "",
        "DATE": "",
        "GENRE": "",
        "COMMENT": "",
        "COMPILATION": "",
        "DISCNUMBER": "",
        "TOTALDISCS": "",
        "ALBUMARTIST": "",
    }
    try:
        with open(cuesheetfile, "r") as file:
            content = file.read()
    except OSError as e:
        print("gettagfromcuesheet: " + str(e), file=sys.stderr)
        sys.exit(1)

    # split the content into tagsection and tracksection
    # use FILE and throw away the rest
    # can use TRACK too
    tagsection, *tracksection = content.split("FILE")
    taglines = tagsection.splitlines()
    for tagline in taglines:
        if tagline.startswith("REM"):
            _, tag, *value = tagline.split(" ")
            tag = tag.upper()
            value = dequote(" ".join(value))
            if tag in tagdict.keys():
                tagdict[tag] = value
        if tagline.startswith("PERFORMER"):
            value = dequote(tagline[10:].strip())
            tagdict["ARTIST"] = value
        if tagline.startswith("TITLE"):
            value = dequote(tagline[6:].strip())
            tagdict["ALBUM"] = value
    return tagdict


def template(tagdict: dict) -> str:
    """
    returns a string which can be used as a template
    """
    t = f"DISCID={tagdict['DISCID']}\n"
    t += f"ARTIST={tagdict['ARTIST']}\n"
    t += f"ALBUM={tagdict['ALBUM']}\n"
    t += f"DATE={tagdict['DATE']}\n"
    t += f"GENRE={tagdict['GENRE']}\n"
    t += f"COMMENT={tagdict['COMMENT']}\n"
    t += f"COMPILATION={tagdict['COMPILATION']}\n"
    t += f"DISCNUMBER={tagdict['DISCNUMBER']}\n"
    t += f"TOTALDISCS={tagdict['TOTALDISCS']}\n"
    t += f"ALBUMARTIST={tagdict['ALBUMARTIST']}\n"
    return t


@click.command()
@click.option("-t", "--tag", "tag", help="Extract the tag information", default=None)
@click.argument("filename", type=click.Path(exists=True, file_okay=True, dir_okay=False))
def cli(tag, filename):
    tagdict = get_tag_from_cuesheet(filename)
    if tag:
        print(tagdict.get(tag.upper(), "<None>"))
    else:
        print(template(tagdict))


if __name__ == f"__main__":
    cli()
