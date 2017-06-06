from __future__ import print_function
from collections import deque
import sys
import os
import csv
from prosody_reaper import ProsodicReaper

class BatchProcess(object):
    """docstring for BatchProcess"""
    def __init__(self, batchFilename, featdumpFilename, debug=True):
        self.batchFilename = batchFilename
        self.featdumpFilename = featdumpFilename
        self.reaper = ProsodicReaper(batchFilename)
        self.debug = debug
        super(BatchProcess, self).__init__()

    def get_last_row(self, csv_filename):
        with open(csv_filename, 'r') as f:
            q = deque(csv.reader(f), 1)
            lastrow = q[0]
            participants = lastrow[0]
            if self.debug:
                # print("Participants: ", participants)
                print("Last Row: ", lastrow)
            return lastrow

    def get_last_participants(self, csv_filename):
        with open(csv_filename, 'r') as f:
            q = deque(csv.reader(f), 1)
            lastrow = q[0]
            if "EOF" in lastrow:
                print("FOUND EOF")
                participants = lastrow.split('|')[1]
            else:
                participants = lastrow[0]
            if self.debug:
                print("Participants: ", participants)
                # print("Last Row: ", lastrow)
            return participants


    # def reapFeaturesList(self):
    #     assert self.fileList is not None
    #     with open(self.fileList) as f:
    #         content = f.readlines()
    #     content = [x.strip() for x in content]
    #     f = open("features4.csv", 'wt')
    #     try:
    #         writer = csv.writer(f)
    #         for file in content:
    #             self.setParticipants(file)
    #             feat = self.reapFeatures()
    #             writer.writerow(feat["MALE"])
    #             writer.writerow(feat["FEMALE"])
        



    def process(self):
        lastrow = self.get_last_row(self.featdumpFilename)
        participants = self.get_last_participants(self.featdumpFilename)
        with open(self.fileList) as f:
            batch = f.readlines()
        batch = [x.strip() for x in batch]

        indexStopped = batch.index(participants+".txt")
        filesRemaining
        f = open("reaped_features.csv", 'a')
        try:
            writer = csv.writer(f)
            for filename in batch:
                self.reaper.setParticipants(filename)
                feat = self.reaper.reapFeatures()
                writer.writerow(feat["MALE"])
                writer.writerow(feat["FEMALE"])
        finally:
            f.close()

    def test(self):
        lastRow = self.get_last_row(self.featdumpFilename)
        participants = self.get_last_participants(self.featdumpFilename)




def main():
    bp = BatchProcess('test_batch1.txt', 'features.csv')
    bp.test()
    bp2.test()

if __name__ == '__main__':
    main()