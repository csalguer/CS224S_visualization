from __future__ import print_function
import librosa
import numpy as np



class ProsodicReaper(object):
    """docstring for ProsodicReaper"""
    def __init__(self, arg):
        super(ProsodicReaper, self).__init__()
        self.arg = arg
        

    def 

    
    def mfcc_recognizer():

        (rate,sig) = wav.read("sample.wav")
        mfcc_feat = mfcc(sig,rate, numcep=56)
        #fbank_feat = logfbank(sig,rate)
        print(mfcc_feat)
        print(mfcc_feat.shape)
        #print(fbank_feat[1:3,:])
        return mfcc_feat

    def

if __name__ == '__main__':
    prosody = ProsodicReaper()
