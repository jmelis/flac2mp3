#!/bin/bash
tmp=./tmp$$.tmp
FLAC="$1"
OUT="$2"
MP3="${FLAC%.flac}.mp3"

echo "from: "$FLAC
echo "to: "$OUT
exit
#> $lame_opts .= '-q 2 '; # Noise shaping: 0 best - 9 worst. 2 is good enuough
#> $lame_opts .= '-V 2 '; # Enable variable bitrate. 4 is the default. Let's be a little bit paranoid.
#> $lame_opts .= '-b 128 '; # minimum bitrate
#> $lame_opts .= '-B 320 '; # maximum bitrate: The maximum of course!
#LAME_OPTS='-m s -q 2 -V 2 -b 128 -B 320'
[ -r "$FLAC" ] || { echo can not read file \"$FLAC\" >&1 ; exit 1 ; } ;
metaflac --export-tags-to=- "$FLAC" | sed 's/=\(.*\)/="\1"/' > $tmp
#cat $tmp
. $tmp
rm $tmp
flac -dc "$FLAC" | lame -m s -q 2 -V 2 -b 128 -B 320 --tt "$Title" \
--tn "$Tracknumber" \
--tg "$Genre" \
--ty "$Date" \
--ta "$Artist" \
--tl "$Album" \
--add-id3v2 \
- "$MP3"
# If you want to erase the original FLAC file, uncomment the following line
#rm "$FLAC"
