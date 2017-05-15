from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import numpy as np

(rate,sig) = wav.read("sample.wav")
mfcc_feat = mfcc(sig,rate, numcep=56)
fbank_feat = logfbank(sig,rate)

print(mfcc_feat)
print(mfcc_feat.shape[0])
print(mfcc_feat.shape[1])
print(mfcc_feat.shape)


#print(fbank_feat[1:3,:])