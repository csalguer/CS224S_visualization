from __future__ import print_function
from collections import deque
from prosody_reaper import ProsodicReaper
from emotional_reaper import getFeatFromSign
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
from freq_reaper import FreqReaper
import scipy.io.wavfile as wav 
import pandas as pandas
from sklearn import datasets, metrics, linear_model, naive_bayes, neighbors, tree, svm, neural_network, externals




class PredictionStreamer(object):
    """docstring for PredictionStreamer"""
    def __init__(self, fileName, utterancesDir=None, debug=True):
        self.fileName = fileName
        if fileName is not None:
            self.participants = fileName.split('.')[0].split('-')
        else:
            self.participants = None
        # DEPRECATED
        self.utterancesDir = utterancesDir
        self.debug = debug
        # CODE BELOW FOR DUMPING, loading creates the specific Classifier() instance
        # self.emotion_model = neighbors.KNeighborsClassifier()
        # self.prosody_model = neural_network.MLPClassifier(shuffle=False, random_state=4)
        self.emotion_model = externals.joblib.load('models/emotions/k_neighbors.pkl')
        self.prosody_model = externals.joblib.load('models/nn2.pkl')
        self.freq_reaper = FreqReaper()
        # super(PredictionStreamer, self).__init__()

    def process(self, PFeatOutput, EFeatOutput, PPredictionsOutput, EPredictionsOutput):
        if self.utterancesDir is not None:
            p_predictions, e_predictions = self.processUtterancesDirHandler()
            print("PREDICITONS LIST: ", predictions)
            return predictions
        else:
            ##MAIN METHOD##
            switchPIndices, switchEIndices = self.processTextGridHandler(PFeatOutput, EFeatOutput)
            self.produce(PFeatOutput, EFeatOutput, PPredictionsOutput, EPredictionsOutput, switchPIndices, switchEIndices)
            print("PREDICITONS LIST: ", predictions)



    def produce(self, PFeatOutput, EFeatOutput, PPredictionsOutput, EPredictionsOutput, switchPIndices, switchEIndices):
        X_prosody = pandas.read_csv(PFeatOutput)
        # X_emotions = pandas.read_csv(EFeatOutput)
        #GET FREQS HERE
        # X_append = freq_reaper.runAll()
        # X = np.hstack((X_prosody, X_append))
        X_emotions = self.emotion_model.predict(X_prosody)
        X_emotions = np.atleast_2d(X_emotions).transpose()
        # X = np.hstack((X_prosody, X_emotions))
        prsdy_predicted = self.prosody_model.predict(X_prosody)
        emote_predicted = self.emotion_model.predict(X_emotions)
        

        for i in switchPIndices:
            prsdy_predicted[i] = 'switch'
        for i in switchEIndices:
            emote_predicted[i] = 'switch'
        print("EMOTE PREDICTIONS: ", emote_predicted)
        print("X EMOTIONS: ", X_emotions)
        print("PRSDY PREDICTIONS: ", prsdy_predicted)
        





    def processTextGridHandler(self, PFeatOutput, EFeatOutput):
        tg_pathname = self.getFilepathForTG()
        wav_pathname = self.getFilepathForWAV()
        timingsForDate = self.getIntervalsFromTG(tg_pathname)
        male_timings = timingsForDate["MALE"]
        female_timings = timingsForDate["FEMALE"]
        total_timings = male_timings + female_timings
        print("MALE T: ", male_timings)
        print("FEMALE: ", female_timings)
        print("TOTAL: ", total_timings)
        sorted_timings = sorted(total_timings, key=lambda tup: tup[0])
        numChannels, numFrames, fs, sig = myWave.readWaveFile(wav_pathname)
        assert numChannels is not 0
        p_vec = []
        e_vec = []
        if self.debug is True:
            print(numChannels, numFrames, fs)
            print("\tFrame Sample Rate: ",fs)
            print("\tData Array Shape: ", sig[0].shape)
            print("\tSORTED Timings ...")
            for t in sorted_timings:
                print("\t\t{}".format(t))
        i = 0
        signal_data = sig[0]
        for (start_t, end_t) in sorted_timings:
            start_index = dspUtil.getFrameIndex(start_t, fs)
            end_index = dspUtil.getFrameIndex(end_t, fs)
            assert start_t is not end_t
            utterance = signal_data[start_index:end_index]
            # print(len(utterance))
            e_vec += self.getFeatForFrameAnimation(utterance, fs, emotionFlag=True)
            p_vec += self.getFeatForFrameAnimation(utterance, fs)
            ## PROSODY FEATURES NOW IN P_VEC ##
            if i < len(sorted_timings) - 1:
                p_vec.append("switch")
                e_vec.append("switch")
                i += 1

        print(p_vec)
        print(e_vec)

        switchPIndices = []
        switchEIndices = []
        dummy = [0] * 10
        header = 'feature1 feature2 feature3 feature4 feature5 feature6 feature7 feature8 feature9 feature10'.split(" ")
        with open(PFeatOutput, "wb") as f1:
            writer = csv.writer(f1)
            for (i, elem) in enumerate(p_vec):
                if i is 0:
                    writer.writerow(header)
                if elem is "switch":
                    switchPIndices.append(i)
                    writer.writerow(dummy)
                else:
                    writer.writerow(elem)
        with open(EFeatOutput, "wb") as f2:
            writer = csv.writer(f2)
            for (i, elem) in enumerate(p_vec):
                if i is 0:
                    writer.writerow(header)
                if elem is "switch":
                    switchEIndices.append(i)
                    writer.writerow(dummy)
                else:
                    writer.writerow(elem)

        return switchPIndices, switchEIndices
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


    def getFeatForFrameAnimation(self,signal_data, fs_rate, emotionFlag=False):
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
            if emotionFlag:
                vec = getFeatFromSign(snippet, fs_rate)
                ret.append(vec)
            else:
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
    ps.process("demo_prosody_feat.csv", "demo_emotion_feat.csv", "demo_p_pred.txt", "demo_e_pred.txt")



if __name__ == '__main__':
    #prosody = ProsodicReaper(fileList="test_batch4.txt")
    #prosody.reapFeaturesList()
    main()