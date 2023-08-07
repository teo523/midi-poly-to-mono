import time as tm
import matplotlib.pyplot as plt
import numpy as np
from pylab import hist, show, xticks
import pandas as pd
import numpy as np
from mido import Message, MidiFile, MidiTrack
import sys
inFile = sys.argv[1]
outFile = sys.argv[2]

#Create new MidiFile where we write track 0 as it is and track 1 
# with monophonic MIDI
inputMidi = MidiFile(inFile)


midCopy = MidiFile()
track0 = inputMidi.tracks[0]
midCopy.tracks.append(track0)

track1 = MidiTrack()
midCopy.tracks.append(track1)

for idx,msg in enumerate(inputMidi.tracks[1]):
    copy = 1
    print(idx)
    
    if msg.type == 'note_on':
        delta = 0
        for i in range(8):
            msg2 = inputMidi.tracks[1][idx - (i + 1)]
            nextMsg = inputMidi.tracks[1][idx - (i)]
            delta = delta + nextMsg.time
            if (msg2.type == 'note_on' and delta < 10):
                copy = 0
                
 
        
    if (copy):
        track1.append(msg)
        print("copied")
    else:
        
        track1.append(Message('control_change', channel=0, control=18, value=0, time=msg.time))
        print("removed Note On")
        clearNoteoff = 1;
        for i in range(40):

            if (idx + (i + 1) < len(inputMidi.tracks[1])):
                
                msg3 = inputMidi.tracks[1][idx + (i + 1)]
                
                if (clearNoteoff == 1 and msg3.type == 'note_off' and msg3.note == msg.note):
                    timeAux = msg3.time
                    inputMidi.tracks[1].pop(idx + (i + 1))
                    inputMidi.tracks[1].insert(idx + (i + 1),Message('control_change', channel=0, control=18, value=0, time=timeAux))
                    print("removed Note Off")
                    clearNoteoff = 0
                    
                    
                
                
            
        
                    
midCopy.save(outFile)
