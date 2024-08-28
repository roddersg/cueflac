#!/usr/bin/env python3

# gettagfromtemplate.py
# 24-07-20
# function: getTagFromTemplate
# returns: tagdict
# requires: file "template"
#   extracts tags from the template file, in the same folder
#   returns a dictionary: tagdict
#   should be used as a function to building the mkmeta.sh script or cuesheet
#
# standalone: gettagfromtemplate.py <-t tag> <-f templatefile>
#   -t tag: extract the value of the tag only
#   -f templatefile: the template file to read, otherwise "template" is used

import re
from datetime import date

import click


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: word.group(0).capitalize(), s)


def get_tag_from_template(templatefile: str = "template") -> dict:
    """
    reads the template file and returns a dictionary of tags
    the default file is template
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
        # read the template file
        with open(templatefile) as f:
            template = f.read()
    except IOError:
        # file not found, file cannot be read error or other file errors
        return None
    # process the lines
    template = template.split("\n")
    for line in template:
        if line.startswith("#"):
            continue
        if len(line.strip()) == 0:
            continue
        if "=" in line:
            tag, value = line.split("=")
            value = value.strip(" ")
            tag = tag.upper()
            # check for artist, switch the "The"
            if tag == "ARTIST":
                if value.startswith("The"):
                    value = value[4:] + ", The"
            if tag == "ALBUMARTIST":
                if value.startswith("The"):
                    value = value[4:] + ", The"
            if tag in tagdict.keys():
                tagdict[tag] = value

    # print("getTagFromTemplate")
    # for k,v in tagdict.items():
    #     print(f"{k:15} = |{v}|")
    return tagdict


@click.command()
@click.option("-t", "--tag", "tag", help="Extract the tag information", default=None)
@click.option(
    "-f",
    "--filename",
    "filename",
    help="template file",
    default="template",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def cli(tag, filename):
    """
    cli to test get_tag_from_template.py
    """
    tagdict = get_tag_from_template(filename)
    if tagdict:
        if tag:
            print(tagdict.get(tag.upper(), "<None>"))
        else:
            print(tagdict)
    else:
        print(tagdict)


if __name__ == "__main__":
    cli()
