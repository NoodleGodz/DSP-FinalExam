from math import floor
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift
import scipy.signal as ss
from scipy.io.wavfile import read,write
from random import gauss
from random import seed

n , data = read("Photo_Stuff/ImageStego.wav")
y=data
seed(2)
wn=[]
for i in range(len(y)):
    wn.append(int(gauss(0.9, 0.1)))
ynoise = [y[i]+wn[i] for i in range(len(y))]
write("Photo_Stuff/ImageStegonoise.wav",n,np.array(ynoise,dtype=data.dtype))