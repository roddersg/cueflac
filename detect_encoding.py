# This script is used to detect the encoding of a file.

import chardet


def detect_encoding(file_path):
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
        confidence = result["confidence"]

        return encoding, confidence


# Example usage:
# file_path = "/home/rodney/Downloads/complete/flac/zzVaya Con Dios (2009) - Comme On Est Venu (Columbia 88697592272, EU)-GP-FLAC/Vaya Con Dios - Comme On Est Venu.cue"
# file_path = "cueflac.py"
file_path = "blanktemplate.sh"
encoding, confidence = detect_encoding(file_path)
print(f"Detected encoding: {encoding} with confidence: {confidence:.2f}")
