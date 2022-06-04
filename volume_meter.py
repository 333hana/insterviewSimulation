from asyncio.windows_events import NULL
from urllib import response
import numpy as np
import librosa
from array import array
from matplotlib import pyplot as plt
import IPython.display as ipd
import numpy as np
from unittest.main import main
import matplotlib.pyplot as plt
from tensorflow.keras.models import model_from_json
from multiprocessing import Process


class volume_meter:
    def __init__(self, path):
        self.FRAME_SIZE = 1024
        self.HOP_LENGTH = 512
        self.path = path
    
    def volume(self,uid):
        #ipd.Audio(self.path)
        debussy, sr = librosa.load(self.path)
        sc_debussy = librosa.feature.spectral_centroid(y=debussy, sr=sr, n_fft= self.FRAME_SIZE, hop_length=self.HOP_LENGTH)[0]
        sc_debussy.shape
        frames = range(len(sc_debussy))
        t = librosa.frames_to_time(frames, hop_length=self.HOP_LENGTH)
        len(t)
        plt.figure(figsize=(7,8))
        plt.axhline(y = 5000, color = 'b', linestyle = 'dashed',label = "threshold of normal volume")
        plt.axhline(y = 1200, color = 'b', linestyle = 'dashed')
        plt.plot(t, sc_debussy, color='r',label = "Intensity of sound")
        plt.xlabel('Time (sec)')
        plt.ylabel('vloume')
        plt.legend(bbox_to_anchor = (0.5, 1.1), loc = 'upper center')
        vm = plt.savefig(uid+'/volume of voice.png')
        return vm

if __name__== "__main__":
    vm = volume_meter('records/output.wav')
    vm.volume("0");
