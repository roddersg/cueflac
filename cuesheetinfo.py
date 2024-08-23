#!/usr/bin/env python3

# cuesheetinfo.py
# Extract information from Cuesheet, return an instance of class Cuesheet
# use is_valid() to check for errors

import re
import sys
from pathlib import Path

import click


def dequote(s: str) -> str:
    """
    removes spaces, quotes, double-quotes from string
    """
    s = s.strip()
    if len(s) > 2 and s[0] == s[-1] and s.startswith(('"', "'")):
        return s[1:-1]
    return s


# Cuesheet class
class Cuesheet:
    def is_valid(self) -> bool:
        """
        Only use if is_valid() is True
        """
        return self.valid

    def __init__(self, filename: str):
        valid = False
        self.extractFromCuesheet(filename)

    def extractFromCuesheet(self, filename: str) -> None:
        """
        Extract the tags and tracks from the cuesheet file
        """
        # fmt:off
        tagdict = { "DISCID": "", "ARTIST": "", "ALBUM": "", "DATE": "",
                    "GENRE": "", "COMMENT": "", "COMPILATION": "",
                    "DISCNUMBER": "", "TOTALDISCS": "", "ALBUMARTIST": "",
                }
        # fmt:on
        # read the cuesheet
        self.cuesheet = filename
        with open(filename, "r") as f:
            content = f.read()
        # split into 2 sections
        tagsection, tracksection = content.split("FILE")
        # process the tags
        tagsection = tagsection.split("\n")
        # remove any blank lines
        tagsection = list(filter(None, tagsection))
        # check for REMs, PERFORMER, TITLE
        pattern = re.compile(r"REM \b(\w+)\b \s*(.*)")
        for tagline in tagsection:
            match = pattern.match(tagline)
            if match is not None:
                # skip the ARTIST and ALBUM
                if match.group(1) in tagdict.keys():
                    # skip the ARTIST and ALBUM
                    if match.group(1) not in ["ARTIST", "ALBUM"]:
                        tagdict[match.group(1)] = dequote(match.group(2))
            else:
                match = re.match(r"PERFORMER\s+(.*)", tagline)
                if match is not None:
                    tagdict["ARTIST"] = dequote(match.group(1))
                else:
                    match = re.match(r"TITLE\s+(.*)", tagline)
                    if match:
                        tagdict["ALBUM"] = dequote(match.group(1))
            # fix albumartist tag only if various artists, previously set usiNG compilation
            if tagdict["COMPILATION"] is not None:
                tagdict["ALBUMARTIST"] = tagdict["ARTIST"]
        # assign to the instance
        self.artist = tagdict["ARTIST"]
        self.album = tagdict["ALBUM"]
        self.albumartist = tagdict["ALBUMARTIST"]
        self.date = tagdict["DATE"]
        self.genre = tagdict["GENRE"]
        self.comment = tagdict["COMMENT"]
        self.compilation = tagdict["COMPILATION"]
        self.discnumber = tagdict["DISCNUMBER"]
        self.totaldiscs = tagdict["TOTALDISCS"]

        # track_section
        tracks = tracksection.split("TRACK")
        # extract the filename of the audio source
        fileline, _ = tracks.pop(0).split("WAVE")
        self.audiosource = dequote(fileline)
        # Process the tracks
        track_info = []
        for track in tracks:
            # print(track)
            track_number = re.search(r"(\d+)", track, flags=re.MULTILINE).group(1)
            title = re.search(r'TITLE "(.*?)"', track).group(1)
            performer = re.search(r'PERFORMER "(.*?)"', track).group(1)
            index = re.findall(r"INDEX\s+01\s+(\d+):(\d+):(\d+)", track)
            track_info.append(
                [
                    int(track_number),
                    dequote(title),
                    dequote(performer),
                    [index[0][0], index[0][1], index[0][2]],
                ]
            )
        self.tracks = track_info
        self.valid = True

    def __repr__(self) -> str:
        # s = f"<Cuesheet object at {hex(id(self))}>"
        s = f"<Cuesheet object: {self.cuesheet}>"
        return s

    def pprint(self, full: bool = False) -> str:
        """
        Prints out cuesheet details
        """
        s = f"{self.cuesheet}\n"
        s += f"Artist       : {self.artist}\n"
        s += f"Album        : {self.album}\n"
        s += f"Album Artist : {self.albumartist}\n"
        s += f"Date         : {self.date}\n"
        s += f"Genre        : {self.genre}\n"
        s += f"Comment      : {self.comment}\n"
        s += f"Compilation  : {self.compilation}\n"
        s += f"Disc Number  : {self.discnumber}\n"
        s += f"Total Discs  : {self.totaldiscs}\n"
        s += f"Audio Source : {self.audiosource}\n"
        if full:
            s += f"Track List:\n"
            for t in self.tracks:
                s += f"  {t}\n"
        return s


# end of Class Cueshet-----------------------------------------------


@click.command()
@click.argument("filename", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("-t", "--tag", "tag", help="Extract the tag information")
@click.option("-v", "--verbose", "verbose", help="Display tags, or more information", count=True)
def cli(filename, tag, verbose):
    cs = Cuesheet(filename)
    if cs.is_valid() == False:
        click.err(f"Invalid Cuesheet: {cs}", err=True)
        sys.exit(1)
    if verbose > 0:
        click.echo(cs.pprint(full=False))
        if verbose > 1:
            click.echo(cs.pprint(full=True))
        return
    # process when no tag is specifed, just return the Cuesheet object
    if tag is None:
        click.echo(cs)
        return
    # process when a tag is specified
    tag = tag.lower()
    if tag == "artist":
        click.echo(cs.artist)
    elif tag == "album":
        click.echo(cs.album)
    elif tag == "albumartist":
        click.echo(cs.albumartist)
    elif tag == "date":
        click.echo(cs.date)
    elif tag == "genre":
        click.echo(cs.genre)
    elif tag == "comment":
        click.echo(cs.comment)
    elif tag == "compilation":
        click.echo(cs.compilation)
    elif tag == "discnumber":
        click.echo(cs.discnumber)
    elif tag == "totaldiscs":
        click.echo(cs.totaldiscs)
    elif tag == "audiosource":
        click.echo(cs.audiosource)
    else:
        click.echo("Unknown tag:", tag)
    # print(cs.pprint())


if __name__ == "__main__":
    cli()
