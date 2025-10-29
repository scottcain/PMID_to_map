#!/usr/bin/perl
use strict;
use warnings;

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
