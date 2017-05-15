from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav
import numpy as np

def mfcc_recognizer():

	(rate,sig) = wav.read("sample.wav")
	mfcc_feat = mfcc(sig,rate, numcep=56)
	#fbank_feat = logfbank(sig,rate)
	print(mfcc_feat)
	print(mfcc_feat.shape)
	#print(fbank_feat[1:3,:])
	return mfcc_feat