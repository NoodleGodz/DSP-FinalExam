from email.mime import audio
from matplotlib.pyplot import imread,imsave, imshow
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft,ifft
import scipy.signal as ss
from scipy.io.wavfile import read,write

def roundcom(a):
    return np.round(a.real,5)+np.round(a.imag,5)*1j
def bintotext(a):
    a=np.reshape(a,(len(a)//8,8)).astype(np.int32)
    b=np.packbits(a)
    c=""
    for i in b:
        c+=chr(int(i)) 
    return c


#Load audio
audiofile ="MusicLong"
audiotail ="_stego.wav"
fs , data = read(audiofile+audiotail)




msglen=167
msgbinlen = 8 * msglen
seglen = int(2**np.ceil(np.log2(2*msgbinlen)))
segnum = int(np.floor(len(data)/seglen))
segmid = seglen // 2



fdata=data.reshape((segnum,seglen))
phi=np.angle(roundcom(fft(fdata)))
phi2 = phi[0,-msgbinlen+segmid:segmid]
d=phi2/-(np.pi/2)
d[d==-1]=0


print("Secret Message:  ")
msg=bintotext(d)
print(msg)



txt=open("Output.txt",'w')
txt.write(msg)
txt.close()

