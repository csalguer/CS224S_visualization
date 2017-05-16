from __future__ import print_function
modulePath = 'cpl_lib/' # change as appropriate
import sys
sys.path.append(modulePath)
# now you're good to import the modules
import generalUtility
import dspUtil
import matplotlibUtil
import librosa
import numpy as np



class ProsodicReaper(object):
    """docstring for ProsodicReaper"""
    def __init__(self, filename="sample.wav"):
        super(ProsodicReaper, self).__init__()
        self.filename = filename
        

    def holdover(self, arg):
        print ("echo")


    def getSelfUtterances(self, )

if __name__ == '__main__':
    prosody = ProsodicReaper()
    prosody.holdover(0)