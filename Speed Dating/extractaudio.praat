# Dan Jurafsky 
# Given audio and textgrid files for speed dates, extract various acoustic features for each interval (turn)

# Input parameters
form Get_AudioFeatures
	text audiofile sound.wav
	text gridfile sound.TextGrid
	text featurefile features.txt
	text genderswitch BOTH
endform

# Set variable values to the default
call defaultvalues

# Confirm that the audio file exists
if (not (fileReadable(audiofile$)))
    printline "audiofile not readable"
    exit
endif
if (not (fileReadable(gridfile$)))
    printline "gridfile not readable"
    exit
endif

filedelete 'featurefile$'

        #for each  speaker (tier)
            #for each uttearnce
               # extract all the features
               # write all the features


# Open audio file
Read from file... 'audiofile$'
soundname$ = selected$ ("Sound")
soundid = selected ("Sound")

# Open the TextGrid:
Read from file... 'gridfile$'
gridname$ = selected$("TextGrid")
gridid = selected("TextGrid")


# Write a row of column titles 
titleline$ = "dateid	turnnum	gender	tnstart	tnend	tndur	pmin	ptmin	pmax	ptmax	pquan	pmean	psd	pslope	pslnjmp	imin	itmin	imax	itmax	iquan	imean	transcript	'newline$'"
fileappend 'featurefile$' 'titleline$'

#titleline$ = "Filename	Gender	Segment label	Maximum pitch (Hz)'newline$'"
#fileappend "'resultfile$'" 'titleline$'

if genderswitch$ = "FEMALE"  or genderswitch$ = "BOTH"
    # Now do the FEMALE tier  first
    femaleMinPitch = 100
    femaleMaxPitch = 425
    select soundid
    To Pitch (ac)... 0.01 femaleMinPitch 15 yes 0.03 0.45 0.01 0.35 0.14 femaleMaxPitch
    pitchid = selected("Pitch")
    
    select soundid
    To Intensity... 100 0 yes
    intensityid = selected("Intensity")
    
    
    # Find the tier number with the name 'FEMALE'
    gender$="FEMALE"
    select gridid
    call GetTier "FEMALE" tier
    numberOfIntervals = Get number of intervals... tier
    
    # For each interval in the FEMALE tier
       for interval to numberOfIntervals
	    transcript$ = Get label of interval... tier interval
	    if transcript$ <> ""
	        # if the interval has an unempty transcript, get its start and end:
		    start = Get starting point... tier interval
		    end = Get end point... tier interval
 	            # Compute interval duration
	            totaldur = end - start
		    # get Pitch feature for that interval
		    call getPfeatures 
		    # get Intensity feature for that interval
		    call getIfeatures 
		    # Save result to text file:
		    call writeoutput
		    select gridid
	    endif
       endfor
endif

if genderswitch$ = "BOTH"
 # Now do the MALE tier 
 
 #First remove the female pitch and intensity tracks and reextract female pitch and intensity
 select pitchid
 Remove
 select intensityid
 Remove
endif

if genderswitch$ = "BOTH" or genderswitch$ = "MALE"
    gender$="MALE"
    
    #First extract a male pitch track
    maleMinPitch = 75
    maleMaxPitch = 300
    select soundid
    To Pitch (ac)... 0.01 maleMinPitch 15 yes 0.03 0.45 0.01 0.35 0.14 maleMaxPitch
    pitchid = selected("Pitch")
    
    select soundid
    To Intensity... 75 0 yes
    intensityid = selected("Intensity")
    
    
    # Find the tier number with the name 'MALE'
    select gridid
    call GetTier "MALE" tier
    numberOfIntervals = Get number of intervals... tier
    
    # For each interval in the MALE tier
       for interval to numberOfIntervals
	    transcript$ = Get label of interval... tier interval
	    if transcript$ <> ""
	        # if the interval has an unempty transcript, get its start and end:
		    start = Get starting point... tier interval
		    end = Get end point... tier interval
 	            # Compute interval duration
	            totaldur = end - start
		    # get Pitch feature for that interval
		    call getPfeatures 
		    # get Intensity feature for that interval
		    call getIfeatures 
		    # Save result to text file:
		    call writeoutput
		    select gridid
	    endif
       endfor
endif



# === PRAAT PROCEDURES===


procedure getPfeatures 
	# Extract PITCH features
        select pitchid
	pmin = Get minimum... 'start' 'end' Hertz Parabolic
	ptmin = Get time of minimum... 'start' 'end' Hertz Parabolic
	pmax = Get maximum... 'start' 'end' Hertz Parabolic
	ptmax = Get time of maximum... 'start' 'end' Hertz Parabolic
	pquan = Get quantile... 'start' 'end' 0.5 Hertz
	pmean = Get mean... 'start' 'end' Hertz
	psd = Get standard deviation... 'start' 'end' Hertz
	pslope = Get mean absolute slope... Hertz
	pslopenojumps = Get slope without octave jumps
endproc

procedure getIfeatures 
	# Extract INTENSITY features
        select intensityid
	imin = Get minimum... 'start' 'end' Parabolic
	itmin = Get time of minimum... 'start' 'end' Parabolic
	imax = Get maximum... 'start' 'end' Parabolic
	itmax = Get time of maximum... 'start' 'end' Parabolic
	iquan = Get quantile... 'start' 'end' 0.5
	imean = Get mean... 'start' 'end' energy
endproc

procedure writeoutput
	# OUTPUT feature values
	# Careful, there are tabs at the end of each line
	textline$ = "'soundname$'	'interval'	'gender$'	'start'	'end'	'totaldur:2'	'pmin:3'	'ptmin:3'	'pmax:3'	'ptmax:3'	'pquan:3'	'pmean:3'	'psd:3'	'pslope:3'	'pslopenojumps:3'	'imin:3'	'itmin:3'	'imax:3'	'itmax:3'	'iquan:3'	'imean:3'	'transcript$' 'newline$'"
	fileappend 'featurefile$' 'textline$'

endproc
	
procedure oldwriteoutput
	# OUTPUT feature values
	# Careful, there are tabs at the end of each line
	print 'soundname$'	
	print 'interval'	

	print 'gender$'	

	print 'start'	
	print 'end'	

	print 'totaldur:2'	
	
	print 'pmin:3'	
	print 'ptmin:3'	
	print 'pmax:3'	
	print 'ptmax:3'	
	print 'pquan:3'	
	print 'pmean:3'	
	print 'psd:3'	
	print 'pslope:3'	
	print 'pslopenojumps:3'	
	
	print 'imin:3'	
	print 'itmin:3'	
	print 'imax:3'	
	print 'itmax:3'	
	print 'iquan:3'	
	print 'imean:3'	
	print 'transcript$'
	print 'newline$'
	
endproc

# Adjust sex parameters for pitch analyses
# Procedure to adjust pitch analyses according to sex
procedure sex_parameters s$
	if s$ = "M"
		sexMinPitch = 75
		sexMaxPitch = 300
		sexMaxFormant = 3500
	elif s$ = "F"
		sexMinPitch = 100
		sexMaxPitch = 425
		sexMaxFormant = 3900
	else
		call writeoutput
		exit Error:	's$' not M or F!
	endif
endproc

procedure defaultvalues
	pmin = -20000
	ptmin = -20000
	pmax = -20000
	ptmax = -20000
	pquan = -20000
	pmean = -20000
	psd = -20000
	pslope = -20000
	pslopenojumps = -20000
	
	imin = -20000
	itmin = -20000
	imax = -20000
	itmax = -20000
	iquan = -20000 
	imean = -20000 
endproc

#-------------
# This procedure finds the number of a tier that has a given label.

procedure GetTier name$ variable$
        numberOfTiers = Get number of tiers
        itier = 1
        repeat
                tier$ = Get tier name... itier
                itier = itier + 1
        until tier$ = name$ or itier > numberOfTiers
        if tier$ <> name$
                'variable$' = 0
        else
                'variable$' = itier - 1
        endif

	if 'variable$' = 0
		exit The tier called 'name$' is missing from the file 'soundname$'!
	endif

endproc

