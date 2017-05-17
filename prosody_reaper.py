from __future__ import print_function
modulePath = 'cpl_lib/' # change as appropriate
import sys
import os
sys.path.append(modulePath)
# now you're good to import the modules
import generalUtility
import dspUtil
import praatTextGrid
import praatUtil
import scipy.io.wavfile as wav 
import myWave
import matplotlibUtil
import librosa
import numpy as np
import csv


class ProsodicReaper(object):
    """docstring for ProsodicReaper"""
    def __init__(self, filename="sample.wav", fileList=None):
        super(ProsodicReaper, self).__init__()
        self.filename = filename
        self.fileList = fileList
        if self.fileList is None:
            participants = self.filename.split('.')[0].split('-')
            print(participants)
            self.participants = participants
        else:
            print(self.fileList)

    

    def reapFeatures(self):
        tg_pathname = self.getFilepathForTG()
        wav_pathname = self.getFilepathForWAV()
        timingsForDate = self.getIntervalsFromTG(tg_pathname)
        male_timings = timingsForDate["MALE"]
        female_timings = timingsForDate["FEMALE"]
        numChannels, numFrames, fs, sig = myWave.readWaveFile(wav_pathname)
        
        assert numChannels is not 0
        print(numChannels, numFrames, fs)
        print("\tFrame Sample Rate: ",fs)
        print("\tData Array Shape: ", sig[0].shape)
        male_vec = self.calculateFeatures(male_timings, fs, sig[0])
        female_vec = self.calculateFeatures(female_timings, fs, sig[0])
        return {"MALE":male_vec, "FEMALE":female_vec}


    def reapFeaturesList(self):
        assert self.fileList is not None
        with open(self.fileList) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        f = open("features3.csv", 'wt')
        try:
            writer = csv.writer(f)
            for file in content:
                self.setParticipants(file)
                feat = self.reapFeatures()
                writer.writerow(feat["MALE"])
                writer.writerow(feat["FEMALE"])
        finally:
            f.close()


    def setParticipants(self, filename):
        self.filename = filename
        participants = filename.split('.')[0].split('-')
        print(participants)
        self.participants = participants


    def calculateFeatures(self, timings, fs_rate, signal_data):
        F0_arr = []
        RMS_arr = []
        for (start_t, end_t) in timings:
            # print("\t(s,e) = ", "(", start_t, ", ", end_t, ")")
            start_index = dspUtil.getFrameIndex(start_t, fs_rate)
            end_index = dspUtil.getFrameIndex(end_t, fs_rate)
            # print("\t\tConverted(s,e) = ", "(", start_index, ", ", end_index, ")")
            assert start_t is not end_t
            utterance = signal_data[start_index:end_index]
            # result =  dspUtil.calculateF0OfSignal(signal_data, fs_rate, tmpDataPath='temp/', \
            #     tStart=start_t, tEnd=end_t)
            F0_result = dspUtil.calculateF0once(utterance, fs_rate)
            RMS_result = dspUtil.calculateRMSOnce(utterance)
            F0_arr.append(F0_result)
            RMS_arr.append(RMS_result)
            # print("F0: ", F0_result)
            # print("RMS: ", RMS_result)
        vec = self.packageFeatures(F0_arr, RMS_arr)
        print(vec)
        return vec
    

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

        # print(F0_min, F0_max, F0_mean, F0_std, F0_range)
        # print(RMS_min, RMS_max, RMS_mean, RMS_std, RMS_range)
        # (rate,sigData) = wav.read(pathname)
        # print(rate, sigData)
        # numChannels, numFrames, fs, data = myWave.readWaveFile(pathname)
        # print(numChannels, numFrames, fs)
        return [F0_min, F0_max, F0_mean, F0_std, F0_range, RMS_min, RMS_max, RMS_mean, RMS_std, RMS_range]


    def getIntervalsFromTG(self, filepath):
        textGrid = praatTextGrid.PraatTextGrid(0, 0)
        # arrTiers is an array of objects (either PraatIntervalTier or PraatPointTier)
        arrTiers = textGrid.readFromFile(filepath)
        # print(arrTiers)
        speakers = {}
        for tier in arrTiers:
            sexOfSpeaker = tier.getName()
            # print(sexOfSpeaker)
            # print(tier.getName())
            # print(tier.getType())
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
                



    def getFilepathForTG(self, rev=False):
        assert self.participants is not None
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

# class F0Features:
#     def __init__(self, F0_min, F0_max, F0_mean, F0_std, F0_range):
#     self.F0_min = F0_min
#     self.F0_max = F0_max
#     self.F0_mean = F0_mean
#     self.F0_std = F0_std
#     self.F0_range = F0_range


if __name__ == '__main__':
    prosody = ProsodicReaper(fileList="test_batch3.txt")
    prosody.reapFeaturesList()