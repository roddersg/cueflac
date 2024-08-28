# cueflac tools
These programs/scripts allow you to convert single flac files (which form an album) into a single flac file using `shntool join` and to generate the cuesheet `shntool cue`.  The tags are then included into the cuesheet which is embedddd into the flac file together with `cover.jpg`

## file/program requirements
- a list of flac files which form the album (\<titles\>.flac)
- the album cover - `cover.jpg` with resolutionm 500x500 px
- the album's song list
- external tools: shntool.exe, metaflac.exe, convert.exe (from imagemagick), sox.exe

### mkj24.sh 
- will use `maketemplate24.sh` to create a template file for you to edit, these are the tags.  Use COMPILATION=1 and fill ALBUMARTIST if you have multiple performers on the album
- `cleanfilelist.py` creates a text filelist (and filelist.org) for you to edit the song titles, performers etccollect, sort the flac files ro form a list `filelist` and `filelist.org`
- if the album has multiple performers, these need to be separated by a '-', which will then be converted to a '|' delimited file.  Check for extra '-' and correct in editor
- `shntool cue` uses `filelist.org` to create a join.cue cuesheet
- `shntool join` will join all the flac files (in `filelist.org`) into a single file - `joined.flac`

```bash
    hntool cue -F filelist.org > joined.cue
    shntool join -F filelist.org -o flac
 ```
- when ready, `cueflac.py` uses joined.cue and tags are converted to \<artist - albumtitle\>.cue, which is embedded into joined.flac together with tags and cover.jpy and then renamed to \<artist - albumtittle\>/flac.
- cover.jpg is also renamed to \<artist - albumtitle\>.jpg
- `movemusic24.sh` is then used to move the files to a folder in ~/Music/done/cdimages

### blanktemplate.sh

- creates a blank template for the music album

### cleanfilelist.py

- creates a listing of the flac files in the working folder. (`filelist.org`).  This list is used to create the cuesheet as well as for the sequence of joining flac files
- makes a copy of `filelist.org` and removes the .flac extension.  If multiple artists, then separate fields using '-' replacing with '|'

### convert_roman.py

- function to convert sequence of roman numerals to caps e.g. Iii => III

### cueflac.py

- uses `template` or any `.cue` files to extract tags and creates `./mkmeta.sh` which is used to embed the tags into the flac file

### cuesheetinfo.py

- reads a cuesheet and generates an object with all the  tags
- not used in the scripts

### detect_encoding.py

- detects they type of file encoding e.g. UTF8-BOM etc.
- as only UTF8 files are used, the others have to be converted before processing can be done.
   not used in the scripts

### fixit24.sh, fixit_here.sh

- for a quick fix of the .cue, .flac, .jpg files
- uses the .cue file to extract the tags and to embed them in the .flac
- you will need a `cover.jpg` file to change the .jpg
- fast fix instead of redoing mkj24.sh
- `fixit_here.sh` fixes the files without moving them to the target folders

### flac2cd24.py

- converts non-compliant 16-44.1K CD flacs to 16/44.1K using `sox.exe`
- re-generates a 1644 version in the folder 1644
- can also call mkj24.sh by transferring the `cover.jpg`, `template` to this folder and calls `mkj24.sh`

### flacinfo.py

- reads a flac file and extracts tags into a Flacinfo object
- checks the validity of the flac file
- see music_catalog project for latest versions of `flacinfo.py`

### gettagfromcuesheet.py

- extracts the tags from the cuesheet and places them into a tagdict() or returns only 1 tag value

### gettagfromtemplate.py

- extracts the tags from the template file and returns a tagdict()
- renames ARTIST, ALBUMARTIST placing "The" at the back

### makecuesheetheader.py, makecuesheettracks.py

- uses tags from tagdict() to create the necessary header for the cuesheet.
- uses joined.cue, filelist.org create the second part of the cuesheet
- used by cueflac.py

### makemetafile.py, makemetafilefromcuesheet.py
- creates the mkmeta.sh file from the tags
- may not be used in cueflac

### maketemplate.sh
- creates the template file from any exiting template and tags
- sequence
    - blank template
    - any existing .cue files
    - any existing template file

### movemusic.sh
- moves the completed .cue, .flac, .jpg files to the target folder
```bash
mkdir "$musicdir"/
    single = ARTIST/DATE-ALBUM
    multiple = various/ARTIST/DATE-ALBUM
    soundtrack = soundtrack/ARTIST/DATE-ALBUM
    christmas = christmas/ARTIST/DATE-ALBUM
mv basename.jpg basename.flac basename.cue TARGET
```

