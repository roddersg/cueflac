#!/usr/bin/env python3

# cleanfilelist.py
# lists the flac files in the current folder
# removes the .flac extension
# changes the filename to Titlecase
# writes out filelist and filelist.org (with .flac)

import re
from pathlib import Path

import click

# def titlecase(text: str) -> str:
#     """
#     Convert a string to title case with apostrophe.
#     """
#     words = text.split()
#     for i in range(len(words)):
#         if "'" in words[i]:
#             # Capitalize the first letter after the apostrophe
#             idx = words[i].index("'") + 1
#             words[i] = words[i][:idx] + words[i][idx:].capitalize()
#         else:
#             words[i] = words[i].capitalize()
#     return " ".join(words)


def title_case(s):
    """
    convert string into title-case
    be mindful of the character after the '
    does not convert bel-reid to Bel-Reid
    does not convert 1st char after (,
    """
    b = []
    for temp in s.split(" "):
        if not temp:
            continue
        if temp[0] in "([{":
            temp = temp[0] + temp[1:].capitalize()
        else:
            temp = temp.capitalize()
        b.append(temp)
    return " ".join(b)


def remove_funny_chars(s: str) -> str:
    s = s.replace("_", " ")
    s = s.replace("?", " ")
    s = s.replace(":", " ")
    s = s.replace('"', "'")
    return s


def convert_roman(text: str) -> str:
    roman_numerals = {
        "i": "I",
        "ii": "II",
        "iii": "III",
        "iv": "IV",
        "v": "V",
        "vi": "VI",
        "vii": "VII",
        "viii": "VIII",
        "ix": "IX",
        "x": "X",
    }

    pattern = r"\b(?:i{1,3}|iv|v|vi{1,3}|ix|x)\b"
    result = re.sub(
        pattern,
        lambda m: roman_numerals.get(m.group().lower(), m.group()),
        text,
        flags=re.IGNORECASE,
    )

    return result


@click.command()
@click.option(
    "-m", "--multiple", "multipleflag", is_flag=True, default=False, help="Multiple Artists"
)
def cleanfilelist(multipleflag: bool = False) -> None:
    p = Path(".")
    flacfiles = sorted(list(p.glob("*.flac")))
    # write out this to filelist.org
    with open("filelist.org", "w") as f:
        for file in flacfiles:
            f.write(f"{file.name}\n")
    # remove the .flac from the filenames
    # change the filenames to Titlecase
    # write out this to filelist, and console
    with open("filelist", "w") as f:
        for file in flacfiles:
            file = file.name
            if file.endswith(".flac"):
                file = file[:-5]
            file = remove_funny_chars(file)
            file = convert_roman(file)
            file = title_case(file)
            if multipleflag:
                n = file.count("-")
                # s = ""
                if n < 2:
                    s = "<"
                elif n == 2:
                    s = ""
                elif n > 2:
                    s = "*" * (n - 2)
                file = s + file.replace("-", "|")
            print(file)
            f.write(f"{file}\n")


if __name__ == "__main__":
    cleanfilelist()
