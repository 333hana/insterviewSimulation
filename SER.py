from asyncio.windows_events import NULL
from urllib import response
import keras
import numpy as np
import librosa
import pyaudio
import wave
from array import array
import time
from matplotlib import pyplot as plt
import IPython.display as ipd
from docx2pdf import convert
import numpy as np
from unittest.main import main
import matplotlib.pyplot as plt
from keras.models import model_from_json
from multiprocessing import Process
import keyboard

session_end=False

class SER():
    
    def __init__(self, path):
        self.path = path
        self.RATE = 24414
        self.CHUNK = 512
        self.RECORD_SECONDS = 20
        self.total_predictions = []
        self.FORMAT = pyaudio.paInt32
        self.CHANNELS = 1
        self.WAVE_OUTPUT_FILE = 'records/output.wav'
        emotions = {'0': 'neutral','1': 'calm','2': 'happy','3': 'sad','4': 'angry','5': 'fearful','6': 'disgust','7': 'surprised'}
        self.emo_list = list(emotions.values())
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

    def load_model(self):
        self.loaded_model = keras.models.load_model(self.path)

    def predictEmotion(self,file):
        data, sr = librosa.load(file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sr, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=1)
        x = np.expand_dims(x, axis=0)
        predictions=self.loaded_model.predict(x,use_multiprocessing=True)
        pred_list = list(predictions)
        pred_np = np.squeeze(np.array(pred_list).tolist(), axis=0) # Get rid of 'array' & 'dtype' statments.
        self.total_predictions.append(pred_np)
        max_emo = np.argmax(predictions)

    def analyse_speech(self,q):
        global session_end 
        self.reset()
        print("at call "+ q+" sessiond end is:",session_end)
        data = array('h', np.random.randint(size = 512, low = 0, high = 500))
        print("** session started")
        while 1:
            print("* recording...")
            frames = [] 
            data = np.nan # Reset 'data' variable.
            while not(session_end): 
                data = array('l',self.stream.read(self.CHUNK)) 
                frames.append(data)
                wf = wave.open(self.WAVE_OUTPUT_FILE, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames)) 
                if keyboard.is_pressed ("q")  :
                     break
            self.predictEmotion(file=self.WAVE_OUTPUT_FILE)   
            # SESSION END 
            if session_end :
                self.stream.stop_stream()
                self.stream.close()
                self.p.terminate()
                wf.close()
                print('** session ended')
                break
            if keyboard.is_pressed ("q")  :
                 break

        # Present emotion distribution for the whole session.
        total_predictions_np =  np.mean(np.array(self.total_predictions).tolist(), axis=0)
        fig = plt.figure(figsize = (7, 5))
        plt.bar(self.emo_list, total_predictions_np, color = 'indigo')
        plt.ylabel("Mean probabilty (%)")
        # qid
        plt.title("Session Summary \n"+"Emotions analyzed for: {(toc - tic):0.4f} seconds")
        ser_result = fig.savefig('imags/Session Summary_speech'+q+'.png')
        return ser_result

    def stop(self):
        global session_end;
        session_end = True

    def reset(self):
        print("reset session end successfully")
        global session_end;
        session_end = False;    


if __name__== "__main__":
    p1 = SER(path='SER_model.h5')
    p1.stop()
    p1.analyse_speech("q")