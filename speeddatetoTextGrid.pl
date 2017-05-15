#!/usr/bin/perl
#   speeddatetoTextGrid.pl
#   Dan Jurafsky
#   convert a ubiqus-labeled speed date transcript into a text grid
#   deals with transcripts that come from two wave files.

#initialize parameters
#
$i=1;
$last_male_endtime = 0;
$last_female_endtime = 0;
$offset = 0;



# Deal with command-line arguments

open(DATEIN, $ARGV[0]) or die("can't open transcript file $ARGV[0]!\n");
$datenumber = $ARGV[0];


# the offset is just added to the relevant times, so figuring
# out whether it should be positive or negative is left to the claling program.
#
#
if  ((scalar(@ARGV) !=  4)  and (scalar(@ARGV) != 1)){
	     die("Usage: speeddatetoTextGrid.pl [wavefile] (maleoffset femaleoffset outfile)\n");
}


if  (scalar(@ARGV) ==  4) {
    $maleoffset = $ARGV[1];
    $femaleoffset = $ARGV[2];
    if (!($maleoffset =~ /-?[0-9][0-9]*\.?[0-9]*/)){
      die("Usage: speeddatetoTextGrid.pl [wavefile] (maleoffset) (femaleoffset) (outfile)\n");
    }
    if (!($femaleoffset !=~ /[-]?[0-9]*\.[0-9]*/)){
      die("Usage: speeddatetoTextGrid.pl [wavefile] (maleoffset) (femaleoffset) (outfile)\n");
    }
   $datenumber = $ARGV[3];
   $datenumber =~ s/.wav//;
   $datenumber =~ s/.TextGrid//;
   $datenumber =~ s/.txt//;
} else {
    $datenumber =~ s/.txt//;
}
$datenumberfile = ">" . $datenumber . ".TextGrid";
open(STDOUT,$datenumberfile) || die("Can't open $datenumberfile for writing");

while(<DATEIN>) {
 chop;
 if (!/[A-Za-z]/) {
   next;
 }
 # remove all lines that start with an /@/, these have known bad times
 if (/^@/) {
     next;
 }
 if (/FILE NAME/) {
   ($junk1,$junk2,$filename) = split(/ /,$_,3);
#   print "file name is $filename\n";
   next;
 }
 if (/AUDIO SOURCE/) {
   ($junk1,$junk2,$junk3) = split(/ /,$_,3);
   next;
 }

 ($time1,$time2,$femalemale,$sentence) = split(/\s+/,$_,4);
 $sentence =~ s/"/'/g;
 if ($time1 =~ /.*:.*:.*\./) {
  $t1 = $time1;
  $t2 = $time2;
  ($junk,$time1) = split(/:/,$t1,2);
  ($junk,$time2) = split(/:/,$t2,2);
 }

 ($minute1,$second1) = split(/:/,$time1);
 ($minute2,$second2) = split(/:/,$time2);
 if ($second2 =~ /\./) {
     $s1 = $second1;
     $s2 = $second2;
     ($second1,$tenth1) = split(/\./,$s1);
     ($second2,$tenth2) = split(/\./,$s2);
 }
 if ($tenth2 ne "") {
     $starttime = $minute1 * 60 + $second1 + $tenth1/10;
     $endtime = $minute2 * 60 + $second2 + $tenth2/10;
    $tenth2="";
 } else {
     $starttime = $minute1 * 60 + $second1 - 0.2;
     if ($starttime < 0) {
	     $starttime = 0;
     }
     $endtime = $minute2 * 60 + $second2 + 0.6;
 }

 if ($femalemale eq "MALE:") {
	 $starttime += $maleoffset;
	 $endtime += $maleoffset;
 } elsif ($femalemale eq "FEMALE:") {
	 $starttime += $femaleoffset;
	 $endtime += $femaleoffset;
 }
 if (($starttime > $endtime) or ($starttime < 0) or ($endtime < 0))  {
    # just ignore any sentences whose end time is before start time.
    # or which are negative because of offsets. usually this means one file starts a few seconds before
    # the other, and the transcript is from the longer file.
    #
    #print STDERR "ERROR IN TIME IN $datenumber;";
    #print STDERR "START ", $starttime, "< END ",$endtime," ", $sentence, "\n";
    next;
}

 $string=$starttime . ":" . $endtime . ":" . $sentence;
 if ($femalemale eq "MALE:") {
     if ($starttime > $last_male_endtime) {
       $silentstring = $last_male_endtime . ":" . $starttime . ":";
       $male[$i++] = $silentstring;
     }
     if ($starttime < $last_male_endtime) {
	     #print STDERR "ERROR IN TIME IN $datenumber;";
	     #print STDERR "Previous turn end:", $last_male_endtime, ", current utt start: ", $starttime, ", sentence #",$sentence, "#\n";
	   # fix starttime and endtime to be same as the last endtime
	   $starttime = $last_male_endtime;
           $string=$starttime . ":" . $endtime . ":" . $sentence;
     }

     $male[$i++] = $string;
     $last_male_endtime = $endtime;
 } elsif ($femalemale eq "FEMALE:") {
     if ($starttime > $last_female_endtime) {
       $silentstring = $last_female_endtime . ":" . $starttime . ":";
#   print "silent female string is $silentstring\n";
       $female[$j++] = $silentstring;
     }
     if ($starttime < $last_female_endtime) {
	     #print STDERR "ERROR IN TIME IN $datenumber;";
	     #print STDERR "Previous turn end:", $last_female_endtime, ", current turn start: ", $starttime, " string is: #", $sentence, "#\n";
	   # fix starttime to be after the last endtime
	   $starttime = $last_female_endtime;
           $string=$starttime . ":" . $endtime . ":" . $sentence;
     }
     $female[$j++] = $string;
     $last_female_endtime = $endtime;
 }
 $finalend = $endtime;
}
$maleintervals = $i-1;
$femaleintervals = $j-1;


print 'File type = "ooTextFile"'."\n";
print 'Object class = "TextGrid"'."\n\n";
print "xmin = 0\n";
print "xmax = $finalend\n";
print "tiers? <exists>\n";
print "size = 2\n";
print "item []:\n";

print "    item [1]:\n";
print '        class = "IntervalTier"'."\n";
print '        name = "MALE"'."\n";
print "        xmin = 0\n";
print "        xmax = $finalend\n";
print "intervals: size = $maleintervals\n";
 
  $last_male_time = 0;
  for ($i=1;$i<=$maleintervals;$i++) {
   $malestring = $male[$i];
   ($malestarttime,$maleendtime,$malesentence) = split(/:/,$malestring,3);

	print "        intervals [$i]:\n";
	print "            xmin = $malestarttime\n";
	print "            xmax = $maleendtime\n";
	print '            text = "'.$malesentence.'"'."\n";
        $last_male_time = $maleendtime;
   }

print "    item [2]:\n";
print '        class = "IntervalTier"'."\n";
print '        name = "FEMALE"'."\n";
print "        xmin = 0\n";
print "        xmax = $finalend\n";
print "intervals: size = $femaleintervals\n";
 
  $last_female_time = 0;
  for ($i=1;$i<=$femaleintervals;$i++) {
   $femalestring = $female[$i];
   chomp($femalestring);
   ($femalestarttime,$femaleendtime,$femalesentence) = split(/:/,$femalestring,3);
   #add an empty interval if needed
	print "        intervals [$i]:\n";
	print "            xmin = $femalestarttime\n";
	print "            xmax = $femaleendtime\n";
	print '            text = "'.$femalesentence.'"'."\n";
        $last_female_time = $femaleendtime;
   }
