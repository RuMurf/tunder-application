from utils import *

SAMPLE_RATE = 44100
FOOTPRINT_SIZE = 30
POINT_EFFICIENCY = 0.8
TARGET_START = 0.05
TARGET_T = 1.8
TARGET_F = 4000
FFT_WINDOW_SIZE = 0.2

sample_rates = [44100]
footprint_sizes = [200]
target_heights = [4000]


directory = "The Number Of The Beast/"
files = ["01 Invaders.wav", "02 Children Of The Damned.wav"]
file = files[1]

id = 1
hashes = []
for file in files:
    hashes += create_fingerprint(directory+file, track_id=id, footprint_size=200, target_height=4000, target_start=1, target_width=6, sample_rate=44100)
    id += 1
save_hashes(hashes, "hashes")

# from madmom.audio import Signal
# from madmom.audio.signal import FramedSignal
# from madmom.audio.stft import STFT
# from madmom.audio.spectrogram import Spectrogram
# import numpy as np
#
# signal = Signal(directory+file, num_channels=1, sample_rate=44100)
# print("samples in signal: "+str(signal.size))
# print("Signal length (seconds): "+str(signal.size/44100))
# framed_signal = FramedSignal(signal, hop_size=441, frame_size=0.2*44100)
# print("frames in signal: "+str(framed_signal.num_frames))
# print("frames per second: "+str(framed_signal.num_frames/275.7))
# stft = STFT(framed_signal)
# print("samples in stft: "+str(stft.size))
# print("sample rate: "+str(stft.size/275.7))
# spectrogram = Spectrogram(stft)
# print("samples in spectrogram: "+str(spectrogram.size))