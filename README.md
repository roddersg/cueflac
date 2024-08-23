# cueflac
Files for creating jpg, flac and cue for my music database 2024 version

mkj

point to musicdir "$HOME/Music/done/images"

if joined.cue or joined.flac exists, remove them

makeTemplate.sh
    use any .cue files, extract tags and add to template
    create a blank template and append to "template"
    call editor to make changes
ask whether single of multiple artists
    cleanfilelist.py <-m>, creates filelist, filelist.org
        filelist.org is a sorted list of .flac files in the folder
        filelist is a sorted list of filenames (split if multiple artists)
open editor
    open template, (*.nfo, *.txt), filelist

join the .flac files
    shntool cue -F filelist.org > joined.cue
    shntool join -F filelist.org -o flac

cueflac.py
    creates ./mkmeta.sh

----Ready
source ./mkmeta.sh
    files ready = basename.jpg, .flac, .cue

move the files
    mkdir "$musicdir"/
        single = ARTIST/DATE-ALBUM
        multiple = various/ARTIST/DATE-ALBUM
        soundtrack = soundtrack/ARTIST/DATE-ALBUM
        christmas = christmas/ARTIST/DATE-ALBUM
    mv basename.jpg basename.flac basename.cue TARGET

flac2cd.sh -- needs to change

tofix:
messages
Enter position of Songs: 9 - should have (1)
Prompts: Multiple (y/N): N (should not prompt N), use back old method
template file, what should be the last?, remove blank lines
