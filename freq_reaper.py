class FreqReaper(object):
    """docstring for ProsodicReaper"""
    def __init__(self, fileList=None):
        super(FreqReaper, self).__init__()
        self.unigram_set = set([])
        self.bigram_set = set([])

    def extractOneUnigramBigram(self, file):
        try:
            with open('speeddating_corpus/transcripts/' + file) as f:
                lines = f.readlines()
        except:
            partial_reversal = file.split("-")
            reversed = partial_reversal[1].split(".")[0] + "-" + partial_reversal[0] + ".txt"
            try:
                with open('speeddating_corpus/transcripts/' + reversed) as f:
                    lines = f.readlines()
            except:
                return
        for line in lines:
            split_line = line.split(":")
            if split_line[0] != 'FILE NAME' and split_line[0] != 'AUDIO SOURCE' and split_line[0].strip() != '' and len(split_line) == 4:
                spoken_line = split_line[3]
                tokenized_line = spoken_line.strip().split()
                for token in tokenized_line:
                    self.unigram_set.add(token)
                for i in range(0, len(tokenized_line) - 1):
                    self.bigram_set.add(tokenized_line[i] + " " + tokenized_line[i + 1])

    def makeAllUnigramBigramSet(self, filename):
        with open(filename) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for file in content:
            self.extractOneUnigramBigram(file)

    def makeUnigramBigramList(self):
        self.unigrams = list(self.unigram_set)
        self.bigrams = list(self.bigram_set)

    def getBigram(self, tokenized_line, bigram_results):
        for i in range(0, len(tokenized_line) - 1):
            bigram = tokenized_line[i] + " " + tokenized_line[i + 1]
            index = self.bigrams.index(bigram)
            if index in bigram_results:
                bigram_results[index] += 1
            else:
                bigram_results[index] = 1
        return bigram_results

    def getUnigram(self, tokenized_line, unigram_results):
        for token in tokenized_line:
            index = self.unigrams.index(token)
            if index in unigram_results:
                unigram_results[index] += 1
            else:
                unigram_results[index] = 1
        return unigram_results

    def getUnigramBigram(self, file):
        try:
            with open('speeddating_corpus/transcripts/' + file) as f:
                lines = f.readlines()
        except:
            return None

        male_unigram_results = dict()
        female_unigram_results = dict()
        male_bigram_results = dict()
        female_bigram_results = dict()
        for line in lines:
            split_line = line.split(":")
            if split_line[0] != 'FILE NAME' and split_line[0] != 'AUDIO SOURCE' and split_line[0].strip() != '' and len(split_line) == 4:
                gender = split_line[2].split()[1]
                spoken_line = split_line[3]
                tokenized_line = spoken_line.strip().split()
                if gender == "MALE":
                    male_unigram_results = self.getUnigram(tokenized_line, male_unigram_results)
                    male_bigram_results = self.getBigram(tokenized_line, male_bigram_results)
                else:
                    female_unigram_results = self.getUnigram(tokenized_line, female_unigram_results)
                    female_bigram_results = self.getBigram(tokenized_line, female_bigram_results)
        return {"MALE_UNIGRAM_RESULTS": male_unigram_results, "FEMALE_UNIGRAM_RESULTS": female_unigram_results,
                "MALE_BIGRAM_RESULTS": male_bigram_results, "FEMALE_BIGRAM_RESULTS": female_bigram_results}

    def writeUnigramBigramToFile(self, f, file):
        results = self.getUnigramBigram(file)
        if results == None:
            partial_reversal = file.split("-")
            reversed = partial_reversal[1].split(".")[0] + "-" + partial_reversal[0] + ".txt"
            results = self.getUnigramBigram(reversed)
            if results == None:
                f.write("\n")
                f.write("\n")
                return
        male_unigram_results = results["MALE_UNIGRAM_RESULTS"]
        for index in sorted(male_unigram_results.keys()):
            f.write(str(index + 1) + ":" + str(male_unigram_results[index]) + " ")
        male_bigram_results = results["MALE_BIGRAM_RESULTS"]
        for index in sorted(male_bigram_results.keys()):
            f.write(str(len(self.unigrams) + index + 1) + ":" + str(male_bigram_results[index]) + " ")
        f.write("\n")

        female_unigram_results = results["FEMALE_UNIGRAM_RESULTS"]
        for index in sorted(female_unigram_results.keys()):
            f.write(str(index + 1) + ":" + str(female_unigram_results[index]) + " ")
        female_bigram_results = results["FEMALE_BIGRAM_RESULTS"]
        for index in sorted(female_bigram_results.keys()):
            f.write(str(len(self.unigrams) + index + 1) + ":" + str(female_bigram_results[index]) + " ")
        f.write("\n")

    def calculateUnigramBigrams(self):
        with open("test_batch1.txt") as f:
            content1 = f.readlines()
        content1 = [x.strip() for x in content1]
        with open("test_batch2.txt") as f:
            content2 = f.readlines()
        content2 = [x.strip() for x in content2]
        with open("test_batch3.txt") as f:
            content3 = f.readlines()
        content3 = [x.strip() for x in content3]
        f = open("freq_features.csv", "w")
        try:
            for file in content1:
                self.writeUnigramBigramToFile(f, file)
            for file in content2:
                self.writeUnigramBigramToFile(f, file)
            for file in content3:
                self.writeUnigramBigramToFile(f, file)
        finally:
            f.close()


if __name__ == '__main__':
    freq_reaper = FreqReaper()
    freq_reaper.makeAllUnigramBigramSet("test_batch1.txt")
    freq_reaper.makeAllUnigramBigramSet("test_batch2.txt")
    freq_reaper.makeAllUnigramBigramSet("test_batch3.txt")
    freq_reaper.makeUnigramBigramList()
    freq_reaper.calculateUnigramBigrams()
