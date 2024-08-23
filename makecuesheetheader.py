#!/usr/bin/env python3

# makeCuesheetHeader.py
# 24-07-20
# makes the header section of the cuesheet file
# uses getTagFromTemplate() to get the tag dictionary from template


def make_cuesheet_header(tagdict: dict) -> str:
    """
    makes the cuesheet header from the tagdict
    """
    taglist = [
        "DISCID",
        "DATE",
        "GENRE",
        "COMMENT",
        "DISCNUMBER",
        "TOTALDISCS",
        "COMPILATION",
        "ALBUMARTIST",
    ]
    header = ""
    for tag in taglist:
        v = tagdict[tag]
        #  print(f"start: |{tag}|{tagdict[tag]}|{type(v)}|")
        # if tagdict[tag] == "":
        #     v = ""
        # else:
        #     try:
        #         v = int(v)
        #     except ValueError:
        #         v = f'"{v}"'
        # remove any spaces if tag is empty--------
        if tagdict[tag]:
            v = ' ' + str(tagdict[tag])

        tagline = f"REM {tag}{v}\n"
        # print(tagline)
        header += tagline
        # print()
    # fix album and albumartist
    if tagdict["ARTIST"].startswith("The "):
        tagdict["ARTIST"] = f"{tagdict['ARTIST'][4:]}, The"
    if tagdict["ALBUMARTIST"].startswith("The "):
        tagdict["ALBUMARTIST"] = f"{tagdict['ALBUMARTIST'][4:]}, The"

    # may have to shift the following to makeCuesheetTracks
    # check whether compilation album
    if tagdict["ALBUMARTIST"]:
        performer = tagdict["ALBUMARTIST"]
    else:
        performer = tagdict["ARTIST"]

    header += f'PERFORMER "{performer}"\n'
    header += f"TITLE \"{tagdict['ALBUM']}\"\n"
    header += f"FILE \"{performer} - {tagdict['ALBUM']}.flac\" WAVE\n"
    # future filenameing
    # header += f"FILE \"{performer}-{tagdict['DATE']}-{tagdict['ALBUM']}.flac\" WAVE\n"
    return header


if __name__ == "__main__":

    from gettagfromtemplate import get_tag_from_template

    tagdict = get_tag_from_template()
    print(make_cuesheet_header(tagdict))
