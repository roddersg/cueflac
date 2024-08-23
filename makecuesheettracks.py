#!/usr/bin/env python3

import re


def make_cuesheet_tracks(tagdict: dict) -> str:
    """
    makes the tracks section of the cuesheet file
    """
    SPACES = 2  # number of spaces for INDENTing
    INDENT = f'{" " * SPACES}'  # INDENT string

    # read the joined file
    with open("joined.cue", "r") as file:
        content = file.read()
    pattern = re.compile(r"\s+TRACK\s+", re.IGNORECASE | re.MULTILINE | re.DOTALL)
    trks = pattern.split(content)
    trks.pop(0)
    # FILE is done in the header section
    trackinfo = []
    for trk in trks:
        t = trk.split("\n")
        nt = []
        for ele in t:
            if ele:
                nt.append(ele.strip())
        trackinfo.append(nt)

    # read in the filenames
    with open("filelist", "r") as file:
        titles = file.read().splitlines()

    # check to see whether both lists are the same length
    if len(titles) != len(trackinfo):
        print("ERROR: lists are not the same length")
        return None

    # spaces = 2
    # INDENT = f'{" " * spaces}'
    if tagdict["ALBUMARTIST"]:
        # multiple artists
        perfpos = int(input("Enter position of performer name (1): ") or "1")
        titlepos = int(input("Enter position of title (2): ") or "2")
        seperator = input("Enter seperator (|) : ") or "|"
        ntitles = []
        for title in titles:
            nt = title.split(seperator)
            ntitles.append(nt)
        # merge the two lists
        tracksection = ""
        for cnt, title in enumerate(ntitles):
            tracksection += f"{INDENT}TRACK {trackinfo[cnt][0]}\n"
            tracksection += f'{INDENT}{INDENT}PERFORMER "{title[perfpos].strip()}"\n'
            tracksection += f'{INDENT}{INDENT}TITLE "{title[titlepos].strip()}"\n'
            for ele in trackinfo[cnt][1:]:
                if ele is not None:
                    tracksection += f"{INDENT}{INDENT}{ele}\n"
    else:
        # single artist
        pos = int(input("Enter position of Songs: ") or "1")
        for i, title in enumerate(titles):
            titles[i] = title[pos - 1 :]
        # merge the two lists
        tracksection = ""
        for cnt, title in enumerate(titles):
            tracksection += f"{INDENT}TRACK {trackinfo[cnt][0]}\n"
            tracksection += f'{INDENT}{INDENT}PERFORMER "{tagdict["ARTIST"]}"\n'
            tracksection += f'{INDENT}{INDENT}TITLE "{title}"\n'
            for ele in trackinfo[cnt][1:]:
                if ele is not None:
                    tracksection += f"{INDENT}{INDENT}{ele}\n"
    return tracksection


if __name__ == "__main__":

    from gettagfromtemplate import get_tag_from_template

    tagdict = get_tag_from_template()
    print(make_cuesheet_tracks(tagdict))
