from __future__ import print_function
from collections import deque
from prosody_reaper import ProsodicReaper
import os
import csv
import sys
modulePath = 'cpl_lib/' # change as appropriate
sys.path.append(modulePath)
# now you're good to import the modules
import math
import myWave
import audioop
import dspUtil
import praatTextGrid
import numpy as np
import scipy.io.wavfile as wav 
from sklearn import datasets, metrics, linear_model, naive_bayes, neighbors, tree, svm, neural_network, externals




class PredictionStreamer(object):
    """docstring for PredictionStreamer"""
    def __init__(self, fileName, utterancesDir=None, debug=True):
        self.fileName = fileName
        if fileName is not None:
            self.participants = fileName.split('.')[0].split('-')
        else:
            self.participants = None
        self.utterancesDir = utterancesDir
        self.debug = debug
        self.emotion_model = externals.joblib.load('models/emotions/k_neighbors.pkl')
        super(PredictionStreamer, self).__init__()

    def process(self):
        if self.utterancesDir is not None:
            predictions = self.processUtterancesDirHandler()
            print("PREDICITONS LIST: ", predictions)
            return predictions
        else:
            predictions = self.processTextGridHandler()
            print("PREDICITONS LIST: ", predictions)

    def processTextGridHandler(self):
        tg_pathname = self.getFilepathForTG()
        wav_pathname = self.getFilepathForWAV()
        timingsForDate = self.getIntervalsFromTG(tg_pathname)
        male_timings = timingsForDate["MALE"]
        female_timings = timingsForDate["FEMALE"]
        total_timings = male_timings + female_timings
        sorted_timings = sorted(total_timings, key=lambda tup: tup[0])
        numChannels, numFrames, fs, sig = myWave.readWaveFile(wav_pathname)
        assert numChannels is not 0
        predictions = []
        if self.debug is True:
            print(numChannels, numFrames, fs)
            print("\tFrame Sample Rate: ",fs)
            print("\tData Array Shape: ", sig[0].shape)
            i = 0
        for (start_t, end_t) in sorted_timings:
            start_index = dspUtil.getFrameIndex(start_t, fs)
            end_index = dspUtil.getFrameIndex(end_t, fs)
            assert start_t is not end_t
            utterance = sig[start_index:end_index]
            predictions.append(self.labelSigByAnimationFrame(fs, sig[0]))
            if i < len(sorted_timings) - 1:
                predictions.append("switch")
                i += 1
        return predictions

    # def processUtterancesDirHandler(self):
        # TODO NOW

    def getIntervalsFromTG(self, filepath):
        textGrid = praatTextGrid.PraatTextGrid(0, 0)
        arrTiers = textGrid.readFromFile(filepath)
        speakers = {}
        for tier in arrTiers:
            sexOfSpeaker = tier.getName()
            intervals = []
            for i in range(tier.getSize()):
                value = tier.get(i)
                start, end, txt = value
                # print("\t", start, end, txt)
                if txt == "":
                    intervals.append((start, end))
            assert len(intervals) is not 0
            speakers[sexOfSpeaker] = intervals
        assert len(speakers) is not 0
        return speakers
                


    def labelSigByAnimationFrame(self, fs_rate, signal_data):
        ret = []
        frames_per_sec = 15.0
        samples_per_frame = fs_rate/frames_per_sec
        iterations = int(math.ceil(len(signal_data) / samples_per_frame))
        for i in xrange(iterations):
            start_index = samples_per_frame * i
            end_index = min(samples_per_frame * (i+1), len(signal_data)-1)
            snippet = signal_data[start_index:end_index]
            #print("[{},{}]:".format(start_index, end_index))
            #print(snippet[0:10])
            vec = self.calculateSubFrameStats(snippet, fs_rate)
            ret.append(vec)
        return ret


    def calculateSubFrameStats(self, snippet, fs_rate):
        F0_arr = []
        RMS_arr = []
        segments = 3
        samples_per_seg = len(snippet)/segments
        iterations = int(math.ceil(len(snippet) / samples_per_seg))
        for i in xrange(iterations):
            start_index = samples_per_seg * i
            end_index = min(samples_per_seg * (i+1), len(snippet)-1)
            subFrame = snippet[start_index:end_index]
            F0_result = dspUtil.calculateF0once(subFrame, fs_rate)
            RMS_result = audioop.rms(subFrame, 2)
            F0_arr.append(F0_result)
            RMS_arr.append(RMS_result)
        return self.packageFeatures(F0_arr, RMS_arr)

    def packageFeatures(self, F0, RMS):
        F0_min = min(F0)
        F0_max = max(F0)
        FSum = sum(F0)
        F0_mean = FSum/len(F0)
        F0_std = np.std(F0)
        F0_range = F0_max - F0_min


        RMS_min = min(RMS)
        RMS_max = max(RMS)
        RSum = sum(RMS)
        RMS_mean = RSum/len(RMS)
        RMS_std = np.std(RMS)
        RMS_range = RMS_max - RMS_min

        return [F0_min, F0_max, F0_mean, F0_std, F0_range, RMS_min, RMS_max, RMS_mean, RMS_std, RMS_range]

    def getFilepathForTG(self, rev=False):
        participants = self.fileName.split('.')[0]
        filepath = 'speeddating_corpus/textgrids/' + "-".join(self.participants) + ".TextGrid"
        rev_filepath = 'speeddating_corpus/textgrids/' + "-".join(reversed(self.participants)) + ".TextGrid"
        if rev:
            return rev_filepath
        return filepath

    def getFilepathForWAV(self, rev=False):
        assert self.participants is not None
        filepath = 'speeddating_corpus/wavefiles/' + "_".join(self.participants) + ".wav"
        rev_filepath = 'speeddating_corpus/wavefiles/' + "_".join(reversed(self.participants)) + ".wav"
        if rev:
            return rev_filepath
        return filepath



def main():
    ps = PredictionStreamer("102-122.txt")
    ps.process()



if __name__ == '__main__':
    #prosody = ProsodicReaper(fileList="test_batch4.txt")
    #prosody.reapFeaturesList()
    main()