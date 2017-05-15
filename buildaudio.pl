#!/usr/bin/perl
#
# buildaudio.pl
#
# Dan Jurafsky
#
# read in a list of TextGrid files, figure out for each
# one what the appropriate wavefile is (only complicated
# because some dates have just a boy wavfile, some
# dates have just girl wavfile, most have both wavefiles) and then call "extractaudio.praat"
# on each conversation side wavfile and matching TextGrid
#
#
#
# read in transcriptlist
#
#@textgrids = <*.TextGrid>;
open(textgridid,"gridlist") or die("cant open gridlist");

while(<textgridid>){
	chop;
        s/.TextGrid//;
	$textgrids{$_} = 1;
}
@wavefiles = <wavfiles/*.wav>;
foreach $wavefile (@wavefiles) {
        $wavefile =~ s/.wav//;
	$wavefile =~ s/.*\///;
	if (($wavefile ne "229_201") and ($wavefile ne "137_107")){
        #print $wavefile,"\n";
	    $waves{$wavefile} = 1;
        } else {
            #print "Skipping ",$wavefile,"\n";
        }
}

foreach $gridfile (sort keys %textgrids) {

	$wavname = "wavfiles/" . converttxttowave($gridfile) . ".wav";
	$gridname = $gridfile . ".TextGrid";
	$featname = $gridfile . ".feat";

	# if this is the only wavefile, call it with BOTH.
	# if there are both wavefiles and ismale,, call it with MALE
	#     else call it with MALE
	#
	if ($waves{converttxttowave($gridfile)} and $waves{converttxttowave(inversedate($gridfile))}) {
	    if (ismale($gridfile)) {
		    $genderswitch = "MALE";
		    $othergenderswitch = "FEMALE";
	    } else {
		    $genderswitch = "FEMALE";
		    $othergenderswitch = "MALE";
	    }

	    # first do first speaker
	    #
	    @args =  ("/Applications/Praat.app/Contents/MacOS/Praat","extractaudio.praat", $wavname, $gridname, $featname,$genderswitch);
	    print "@args" ,"\n";
	    system(@args);

	    # now do second speaker

	    $wavname = "wavfiles/" . converttxttowave(inversedate($gridfile)) . ".wav";
	    $gridname = inversedate($gridfile) . ".TextGrid";
	    $featname = inversedate($gridfile) . ".feat";
	    @args =  ("/Applications/Praat.app/Contents/MacOS/Praat","extractaudio.praat", $wavname, $gridname, $featname,$othergenderswitch);
	    print "@args" ,"\n";
	    system(@args);
	} elsif ($waves{converttxttowave($gridfile)} and !$waves{converttxttowave(inversedate($gridfile))}) {
    	    $genderswitch = "BOTH";
	    @args =  ("/Applications/Praat.app/Contents/MacOS/Praat","extractaudio.praat", $wavname, $gridname, $featname,$genderswitch);
	    print "@args" ,"\n";
	    system(@args);
	} elsif (!$waves{converttxttowave($gridfile)} and $waves{converttxttowave(inversedate($gridfile))}) {
	    if (ismale(inversedate($gridfile))) {
		    $genderswitch = "MALE";
	    } else {
		    $genderswitch = "FEMALE";
	    }
 	     printf "error (warning) couldn't find wave file %s, using %s\n",converttxttowave($gridfile),converttxttowave(inversedate($gridfile));
	     $wavname = "wavfiles/" . converttxttowave(inversedate($gridfile)) . ".wav";
	     $gridname = inversedate($gridfile) . ".TextGrid";
	     $featname = inversedate($gridfile) . ".feat";
	     @args =  ("/Applications/Praat.app/Contents/MacOS/Praat","extractaudio.praat", $wavname, $gridname, $featname,$genderswitch);
	     print "@args" ,"\n";
	     system(@args);
	 } elsif (!$waves{converttxttowave($gridfile)} and !$waves{converttxttowave(inversedate($gridfile))}) {
		 printf "error: couldn't find wave file %s\n",converttxttowave(inversedate($gridfile));
		 next;
	 }

} 

sub canonicalizedate {
	 my ($date) = @_;
	 ($one,$two) = split(/-/,$date);
	 if ($one < $two) {
		 return $date;
	 } else {
		 return $two . "-" . $one;
	 }
}
sub inversedate {
	 my ($date) = @_;
	 ($one,$two) = split(/-/,$date);
	 return $two . "-" . $one;
}
sub convertwavetotxt {
	 my ($date) = @_;
	 ($one,$two) = split(/_/,$date);
	 return $one . "-" . $two;
}
sub converttxttowave {
	 my ($date) = @_;
	 ($one,$two) = split(/-/,$date);
	 return $one . "_" . $two;
}
sub ismale {
	 my ($date) = @_;
#	 print "is $date male?\n";
	 ($one,$two) = split(/-/,$date);
	 if ($one < $two) { 
#		  print "yes\n";
		 return 1;
	 } else {
#		  print "no\n";
		 return 0;
	 }
}
