#!/usr/bin/env python3

import re
import sys


def convert_roman(text):
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


if __name__ == "__main__":
    for line in sys.stdin:
        converted_line = convert_roman(line)
        sys.stdout.write(converted_line)
