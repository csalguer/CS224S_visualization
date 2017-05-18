import csv

class OutcomesReaper(object):
    """docstring for ProsodicReaper"""
    def __init__(self, fileList=None):
        super(OutcomesReaper, self).__init__()

    def setParticipants(self, filename):
        self.filename = filename
        participants = filename.split('.')[0].split('-')
        print(participants)
        self.participants = participants

    def getOutcomes(self):
        assert self.participants is not None
        f = open("speeddating_corpus/speeddateoutcomes.csv", "r")
        male_outcome = -1
        female_outcome = -1
        all_lines = f.readlines()
        for line in all_lines:
            split_line = line.split(",")
            if split_line[0] == self.participants[0] and split_line[1] == self.participants[1]:
                male_outcome = split_line[5]
            elif split_line[0] == self.participants[1] and split_line[1] == self.participants[0]:
                female_outcome = split_line[5]
            elif male_outcome != -1 and female_outcome != -1:
                break
        return {"MALE_OUTCOME": male_outcome, "FEMALE_OUTCOME": female_outcome}


    def getAllOutcomes(self):
        with open("test_batch1.txt") as f:
            content1 = f.readlines()
        content1 = [x.strip() for x in content1]
        with open("test_batch2.txt") as f:
            content2 = f.readlines()
        content2 = [x.strip() for x in content2]
        f = open("outcomes.csv", 'wt')
        try:
            writer = csv.writer(f, lineterminator="\n")
            for file in content1:
                self.setParticipants(file)
                outcomes = self.getOutcomes()
                writer.writerow(outcomes["MALE_OUTCOME"])
                writer.writerow(outcomes["FEMALE_OUTCOME"])
            for file in content2:
                self.setParticipants(file)
                outcomes = self.getOutcomes()
                writer.writerow(outcomes["MALE_OUTCOME"])
                writer.writerow(outcomes["FEMALE_OUTCOME"])
        finally:
            f.close()


if __name__ == '__main__':
    outcome_reaper = OutcomesReaper()
    outcome_reaper.getAllOutcomes()
