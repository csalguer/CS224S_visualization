from __future__ import print_function
modulePath = 'cpl_lib/' # change as appropriate
import sys
import os
sys.path.append(modulePath)
# now you're good to import the modules
import generalUtility
import dspUtil
import praatTextGrid
import myWave
import matplotlibUtil
import librosa
import numpy as np



class ProsodicReaper(object):
    """docstring for ProsodicReaper"""
    def __init__(self, filename="sample.wav", fileList=None):
        super(ProsodicReaper, self).__init__()
        self.filename = filename
        self.fileList = fileList
        if self.fileList is None:
            participants = self.filename.split('.')[0].split('-')
            print(participants)
            dir = os.path.dirname(__file__)
            self.participants = participants
        else:
            print(self.fileList)

    def holdover(self, arg):
        print ("echo")


    def processFirstParticipant(self):
        assert self.participants is not None
        



if __name__ == '__main__':
    prosody = ProsodicReaper(filename="102-122.txt")
    prosody.processFirstParticipant()