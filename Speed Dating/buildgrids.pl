#!/usr/bin/perl
#
# buildgrids.pl
# 2011, Dan Jurafsky
# Given a text transcript (from the list in transcriptlist)
# and a wavefile (from wavfilelist) convert the text transcript to a TextGrid.
# Because when possible we want to take the women's and men's speech info from their individual recordings,
# and because the men's and women's transcript times are taken only from one file, but the recordings are not time-aligned,
# we need to add an offset to the transcript times for one of the transcripts so that the wavefile match the transcript.
# The offsets are in offsetlist.csv.
#
# This means that later, when extracting audio features, we'll
# need to pull the male audio from the man's file (if it exists)
# but the female audio from the female's file (if it exists).
#
#
# read in transcriptlist
#
open(transcriptlist, "./transcriptlist") or die("Can't open ./transcriptlist!\n");

while(<transcriptlist>){
	chop;
	s/.wav//;
	s/.txt//;
	#$date=canonicalize($_);
	$dates{$_} = 1;
	$offsetlist{$_} = -9999;
}



# read in splitlist
#
open(splitlistid, "./splitlist.csv") or die("Can't open ./splitlist.csv!\n"); 
while(<splitlistid>){
	chop;
	s/.wav//;
	s/.txt//;
	($date,$whethersplit) = split(/,/,$_,2);
	$splitlist{$date} = $whethersplit;
}

#
#
# read in skiplist
open(skiplistid, "./skiplist.csv") or die("Can't open ./skiplist.csv!\n");
while(<skiplistid>){
	chop;
	s/ .*//;   # strip off the comments (which say why we are skipping the file)
	s/.wav//;
	s/.txt//;
	$skiplist{$_} = 1;
}
# 
#
# read in offsetlist
open(offsetlistid, "./offsetlist.csv") or die("Can't open ./offsetlist.csv!\n");
while(<offsetlistid>){
	chop;
	s/.wav//;
	s/.txt//;
	s/_/-/;
	($date,$offset) = split(/,/,$_,2);
	$offsetlist{$date} = $offset;
	$offsetlist{inversedate($date)} = $offset;
	#print "offsetlist(",$date,") is ", $offsetlist{$date},"\n";
}

#read in wavfilelist
open(wavfilelistid, "./wavfilelist") or die("Can't open ./wavfilelist!\n");
while(<wavfilelistid>){
	chop;
	s/.wav//;
	s/.txt//;
	$date= convertwavetotxt($_);
	$wavfilelist{$date} = 1;
	#print "wavfilelist(",$date,") is ", $wavfilelist{$date},"\n";
}

foreach $transcript (sort keys %dates) {
 #    $transcript =~ s/anon_//;
	if ($skiplist{$transcript}) {
            #print "skipping $transcript\n";
	    next;
        } else {
            #print "doing $transcript\n";
        }
   # if both wavefiles exist, create two textgrids
    if ((exists $wavfilelist{$transcript}) and exists $wavfilelist{inversedate($transcript)})  {
    #print"both wavefiles exist for $transcript, create two textgrids\n";
	    $offset = $offsetlist{$transcript};
	    # if there is no offset yet for this file
	    if ($offset == -9999) {
		    #printf "No offset yet for file %s\n",$transcript;
	            next;
            }
	    if ($splitlist{$transcript} == 1) {
              # transcript is just from one wavefile
              #print "but transcript is just from one wavefile\n";
                 @args =  ("./speeddatetoTextGrid.pl",$transcript . ".txt", 0, 0, $transcript);
                 #print "@args","\n";
                 system(@args);
                 if (ismale(inversedate($transcript))) {
			 #print "since i'm printing the male other file, flip the offset $offset\n";
                     @args = ("./speeddatetoTextGrid.pl",$transcript . ".txt" ,-$offset,-$offset,inversedate($transcript));
	         }else {
			 #print "since i'm printing the female other file, dont flip the offset\n";
                     @args = ("./speeddatetoTextGrid.pl",$transcript . ".txt" ,$offset,$offset,inversedate($transcript));
	         }
                 #print "@args","\n";
                 system(@args);
             } else  {#if transcript is from two separate wavefiles, 
              #print "and transcript is from both wavefiles\n";
        #for main speaker
	   if (ismale($transcript)) {
              #print "and main speaker is a male\n";
               @args = ("./speeddatetoTextGrid.pl",$transcript . ".txt", 0,$offset,$transcript);
           } else {
              #print "and main speaker is a female\n";
               @args = ("./speeddatetoTextGrid.pl",$transcript . ".txt", $offset,0 ,$transcript);
           }
                 #print "@args","\n";
          system(@args);
        #for other speaker
	   if (ismale(inversedate($transcript))) {
              #print "and other speaker is a male\n";
               @args = ("./speeddatetoTextGrid.pl",$transcript . ".txt", 0, -$offset, inversedate($transcript));
           } else {
              #print "and other speaker is a female\n";
               @args = ("./speeddatetoTextGrid.pl",$transcript . ".txt", $offset, 0, inversedate($transcript));
           }
                 #print "@args","\n";
          system(@args);
	   }
   #  else create one textgrid
   #   from the first speaker if it's there
    } elsif ($wavfilelist{$transcript}) {
          @args = ("./speeddatetoTextGrid.pl",$transcript . ".txt");
                 #print "@args","\n";
          system(@args);
   #   or, oddly, from the second if the transcriber accidentally ordered the date name wrong
  } elsif ($wavfilelist{inversedate($transcript)}) {
      #print("why am i creating wavefile from second speaker?\n");
	  @args = ('./speeddatetoTextGrid.pl', $transcript . ".txt");
                 #print "@args","\n";
          system(@args);
  }
  }

#foreach $file (@files) {
#print $file . "\n";
#}

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
	 #print "is $date male?\n";
	 ($one,$two) = split(/-/,$date);
	 if ($one < $two) { 
		  #print "yes\n";
		 return 1;
	 } else {
		  #print "no\n";
		 return 0;
	 }
}
