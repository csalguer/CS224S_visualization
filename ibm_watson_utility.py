from __future__ import print_function 
import sys 
import os 
from sys import byteorder 
from array import array 
from struct import pack 
import json 
from watson_developer_cloud import TextToSpeechV1 
from watson_developer_cloud import SpeechToTextV1 
import wave 
import pyaudio 
 
 
class IBMWatsonUtility(object): 
    """docstring for IBMWatsonUtility""" 
    def __init__(self): 
        super(IBMWatsonUtility, self).__init__() 
        self.TTS = TextToSpeechV1( 
            username='6681dd9c-1d0d-42e9-bec4-d0cdbebe14d5', 
            password='7A44PekScMqO', 
            x_watson_learning_opt_out=False) 
        self.STT = SpeechToTextV1( 
            username='9d842189-2fb1-4d72-99fe-9d17c6f27ba3', 
            password='RAmSGbTpNStF', 
            x_watson_learning_opt_out=False) 
        self.threshold = 500 
        self.chunk_size = 1024 
        self.format = pyaudio.paInt16 
        self.rate = 44100 
 
    def printVoices(self): 
        jsonVoicesObj = self.TTS.voices() 
        print(json.dumps(jsonVoicesObj, indent = 2)) 
        # return(json.load(jsonVoicesObj)) 
 
    def printSModels(self): 
        jsonSModelsObj = self.STT.models() 
 
 
    def createSpokenWAV(self, text): 
        try: 
            winPath = os.path.join(os.getcwd(), 'resources\\temp\\output.wav') 
            relPath = 'resources/temp/output.wav' 
            with open(relPath, 'wb') as audio_file: 
                audio_file.write(self.TTS.synthesize(text, accept='audio/wav', 
                        voice="en-US_AllisonVoice")) 
            print("Voice_synth: COMPLETE") 
            return relPath 
        except IOError: 
            print("Error in voice_synth creation") 
            return None 
 
 
    def utterPhrase(self, text): 
        assert text is not None 
        path = self.createSpokenWAV(text) 
        if path is None: 
            print("[Error]: Couldn't find file location for temp utterance") 
            return False 
        print("Attempting to play: ", path) 
        self.__playbackUtterance(path) 
        return True 
 
 
    def hearPhrase(self, audioName): 
        assert audioName is not None 
        try: 
            winPath = os.path.join(os.getcwd(), 'resources\\temp\\input.wav') 
            relPath = 'resources/temp/input.wav' 
            with open(relPath, 'rb') as audio_file: 
                jsonResponse = self.STT.recognize(audio_file, content_type='audio/wav', 
                    timestamps=True, word_confidence=True) 
                print("RESPONSE\n\n", json.dumps(jsonResponse)) 
                # audio_file.write(self.TTS.synthesize(text, accept='audio/wav', 
                #         voice="en-US_AllisonVoice")) 
            print("Hearing and transcription: COMPLETE") 
            return relPath 
        except IOError: 
            print("Error in hearing phrase") 
            return None 
    
 
    def is_silent(self, snd_data): 
        "Returns 'True' if below the 'silent' self.threshold" 
        return max(snd_data) < self.threshold 
 
    def normalize(self, snd_data): 
        "Average the volume out" 
        maximum = 16384 
        times = float(maximum)/max(abs(i) for i in snd_data) 
 
        r = array('h') 
        for i in snd_data: 
            r.append(int(i*times)) 
        return r 
 
    def trim(self, snd_data): 
        "Trim the blank spots at the start and end" 
        def _trim(snd_data): 
            snd_started = False 
            r = array('h') 
 
            for i in snd_data: 
                if not snd_started and abs(i)>self.threshold: 
                    snd_started = True 
                    r.append(i) 
 
                elif snd_started: 
                    r.append(i) 
            return r 
 
        # Trim to the left 
        snd_data = _trim(snd_data) 
 
        # Trim to the right 
        snd_data.reverse() 
        snd_data = _trim(snd_data) 
        snd_data.reverse() 
        return snd_data 
 
    def add_silence(self, snd_data, seconds): 
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)" 
        r = array('h', [0 for i in range(int(seconds*self.rate))]) 
        r.extend(snd_data) 
        r.extend([0 for i in range(int(seconds*self.rate))]) 
        return r 
 
    def record(self): 
        """ 
        Record a word or words from the microphone and  
        return the data as an array of signed shorts. 
 
        Normalizes the audio, trims silence from the  
        start and end, and pads with 0.5 seconds of  
        blank sound to make sure VLC et al can play  
        it without getting chopped off. 
        """ 
        p = pyaudio.PyAudio() 
        stream = p.open(format=self.format, channels=1, rate=self.rate, 
            input=True, output=True, 
            frames_per_buffer=self.chunk_size) 
 
        num_silent = 0 
        snd_started = False 
 
        r = array('h') 
 
        while 1: 
            # little endian, signed short 
            snd_data = array('h', stream.read(self.chunk_size)) 
            if byteorder == 'big': 
                snd_data.byteswap() 
            r.extend(snd_data) 
 
            silent = self.is_silent(snd_data) 
 
            if silent and snd_started: 
                num_silent += 1 
            elif not silent and not snd_started: 
                snd_started = True 
 
            if snd_started and num_silent > 30: 
                break 
 
        sample_width = p.get_sample_size(self.format) 
        stream.stop_stream() 
        stream.close() 
        p.terminate() 
 
        r = self.normalize(r) 
        r = self.trim(r) 
        r = self.add_silence(r, 0.5) 
        return sample_width, r 
 
    def record_to_file(self, path): 
        "Records from the microphone and outputs the resulting data to 'path'" 
        sample_width, data = self.record() 
        data = pack('<' + ('h'*len(data)), *data) 
 
        wf = wave.open(path, 'wb') 
        wf.setnchannels(1) 
        wf.setsampwidth(sample_width) 
        wf.setframerate(self.rate) 
        wf.writeframes(data) 
        wf.close() 
    # 
    # NOTE: 
    #   Private method, to be made public if creation of wav per utterance is 
    #   Too expensive 
    # 
    def __playbackUtterance(self, pathname):  
        self.chunk_size = 1024   
        f = wave.open(pathname,"rb") 
        p = pyaudio.PyAudio()  
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()), 
                        channels = f.getnchannels(), 
                        rate = f.getframerate(), 
                        output = True) 
        data = f.readframes(self.chunk_size) 
        while data:   
            stream.write(data) 
            data = f.readframes(self.chunk_size) 
        stream.stop_stream() 
        stream.close() 
        p.terminate() 
 
 
### EXAMPLE USAGE ### 
def main(): 
    ibm = IBMWatsonUtility() 
    ibm.printVoices() 
    ibm.utterPhrase("Hello which would you like to play? :") 
    ibm.utterPhrase("\tNumber one, Tiltbrush") 
    ibm.utterPhrase("\tNumber two, Bioshock") 
    ibm.utterPhrase("\tNumber three, MOBIUS FINAL FANTASY") 
    ibm.utterPhrase("\tOr Number four, nosgoth?") 
 
    print("Please speak into the microphone.") 
    inputLocation = 'resources/temp/input.wav' 
    ibm.record_to_file(inputLocation) 
    print("Sound heard was saved to: ", inputLocation) 
    ibm.hearPhrase(inputLocation) 
 
 
if __name__ == "__main__": 
    main() 