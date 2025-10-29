#!/usr/bin/perl
use strict;
use warnings;

# This script takes a file as it's only argument that contains
# affiliation info from author_location.py script, one per line.
# It then calls the geocode_single.py script iteratively trimming off
# the beginning of the string up to the first comma (then the second, etc)
# until it returns a lat,long pair. This is then written to a file
# along with the original query string. If it fails to find a geolocation
# for a string, it writes "FAILED" to the file.

my $FILEIN = $ARGV[0];
open IN, "<$FILEIN" or die "couldn't open $FILEIN: $!";
my $FILEOUT = $FILEIN.'.locs';
open OUT, ">>$FILEOUT" or die "couldn't open $FILEOUT for writing: $!";

while (<IN>) {
    my $in = $_;
    chomp $in;

    my $loc = resursive_finder($in);

    print OUT "$loc\t$in\n";
    sleep 10;
}
close IN;
close OUT;

sub resursive_finder {
    my $in = shift;

    my @result = `python geocode_single.py $in`;

    if ($result[2] =~ /FAILED/) {
        if ($in =~ s/^[^,]+,\s*(.*)/$1/) {
            sleep 5;
            return resursive_finder($in);
        } 
        else {
            return "FAILED\n"; 
        }
    } else {
        print @result;
    }

    my $coord = $result[6];
    chomp $coord;
    $coord =~ s/Coordinates: //;
    return $coord;
}
