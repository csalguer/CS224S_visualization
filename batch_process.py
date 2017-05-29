from __future__ import print_function
from collections import deque
import sys
import os
import csv
import prosody_reaper

class BatchProcess(object):
    """docstring for BatchProcess"""
    def __init__(self, batchFilename, featdumpFilename):
        self.batchFilename = batchFilename
        self.featdumpFilename = featdumpFilename
        super(BatchProcess, self).__init__()


    def reapFeaturesList(self):
        with open(self.batchFilename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        f = open(self.featdumpFilename, 'a')
        try:
            writer = csv.writer(f)
            for file in content:
                self.setParticipants(file)
                feat = self.reapFeatures()
                writer.writerow(feat["MALE"])
                writer.writerow(feat["FEMALE"])
        finally:
            f.close()


	def get_last_row(self, csv_filename):
	    with open(csv_filename, 'r') as f:
	        try:
	           q = deque(csv.reader(f), 1)
                lastrow = q[0]
                print(lastrow)
                if lastrow[0] == "[EOF]":
                    lastrow = q[1]
                    penultimate = q[2]
                else:
                    penultimate = q[1]
                participants = (lastrow[0], penultimate[0])
            except IndexError:  # empty file
                return None

            for elem in lastrow:
                print(elem)
            print(participants)
            return lastrow

    def __get_next_to_process(self):
        print("echo")

    def test(self):
        self.get_last_row(self.featdumpFilename)


def main():
    bp = BatchProcess('test_batch1.txt', 'features.csv')
    bp.test()

if __name__ == '__main__':
    main()