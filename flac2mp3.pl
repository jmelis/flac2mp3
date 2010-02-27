#!/opt/local/bin/perl
#
# Converts FLAC to MP3 preserving tags
# License: GPLv2
# Home: http://www.GuruLabs.com/downloads.html
#
# Note: Only use on flac files that you trust. A
# malicious ID3v1 tag could hose you.
#

use MP3::Info;

# Lame quality
$lame_opts  = '-m s '; # simple stereo
$lame_opts .= '-q 2 '; # Noise shaping: 0 best - 9 worst. 2 is good enough
$lame_opts .= '-V 2 '; # Enable variable bitrate. 4 is the default. Let's be a little bit paranoid.
$lame_opts .= '-b 128 '; # minimum bitrate
$lame_opts .= '-B 320 '; # maximum bitrate: The maximum of course!

foreach $file (@ARGV) {
  if (!($file =~ /\.flac$/)) {
    print "Skipping $file\n";
    next;
  }
  undef $year; undef $artist; undef $comment; undef $album; undef $title; undef $genre; undef $tracknum;
  if ($tag = get_mp3tag($file)) {
    $year = $tag->{YEAR};
    $artist = $tag->{ARTIST};
    $comment = $tag->{COMMENT};
    $album = $tag->{ALBUM};
    $title = $tag->{TITLE};
    $genre = $tag->{GENRE};
    $tracknum = $tag->{TRACKNUM};
    chomp($year, $artist, $comment, $album, $title, $genre, $tracknum);
    $tracknum = sprintf("%2.2d", $tracknum);
  } else {
    print "Couldn't get id3v1 tag for $file.\n";
  } 
  if (($artist) && ($title) && ($tracknum)) {
     $outfile = "$tracknum" . "_-_" . "$title.mp3";
	 `flac -c -d "$file" | lame $lame_opts --ty $year --ta "$artist" --tc "$comment" --tl "$album" --tt "$title" --tg "$genre" --tn $tracknum - "$outfile"`;
  } else {
    $outfile = $file;
    $outfile =~ s/\.flac$/.mp3/;
	`flac -c -d "$file" | lame $lame_opts - "$outfile"`;
  }
}
