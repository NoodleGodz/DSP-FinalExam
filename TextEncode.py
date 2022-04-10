from matplotlib.pyplot import imread,imsave, imshow
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft,ifft
import scipy.signal as ss
from scipy.io.wavfile import read,write

def roundcom(a):
    return np.round(a.real,5)+np.round(a.imag,5)*1j

def inttofloat32(a:np.ndarray):
    data=np.iinfo(a.dtype)
    khoang=2
    khoangchia=data.max-data.min
    k=khoang/khoangchia
    v=[i*k for i in a]
    v=np.array(v,np.float32)
    return v


#Load audio
audiofile ="Text_Stuff/Input_4"
fs , data = read(audiofile+".wav")
print(data.dtype)
if data.dtype!=np.float32:
    data=inttofloat32(data)

#if that is a stereo file, take right channel
if np.ndim(data)==2:
    data=data[:,1]

#Load text
textfile='Text_Stuff/texttostego.txt'
txt=open(textfile,'r')
msg=txt.read()
txt.close()

#Convert text into Binary
msgbin = np.ravel([[int(y) for y in format(ord(x), '08b')] for x in msg])
msgbinlen=len(msgbin)



seglen = int(2**np.ceil(np.log2(2*msgbinlen)))
segnum = int(np.floor(len(data)/seglen))
print(seglen * segnum <= len(data))

#Convert Binary into Phi (0==pi/2 and 1==-pi/2)
msgPhi = msgbin.copy()
msgPhi[msgPhi == 0] = -1
msgPhi = msgPhi * -(np.pi/2)


#Create segments
segments = data[0:segnum*seglen].reshape((segnum,seglen))
fsegments = fft(segments)
fsegments = roundcom(fsegments)
A = np.absolute(fsegments)
Phi = np.angle(fsegments)
NewPhi=Phi.copy()


#Calculate the difference in each segments
DeltaPhi=np.diff(Phi,axis=0)

#Put the PhiBinary into the first segment
segmid = seglen // 2
NewPhi[0,-msgbinlen+segmid:segmid] = msgPhi
NewPhi[0,segmid+1:segmid+1+msgbinlen] = -msgPhi[::-1]

#Reconstuct the Phi matrix 
for i in range(1, segnum): 
    NewPhi[i,:] = NewPhi[i-1,:] + DeltaPhi[i-1,:]


#Ifft back to time domain
coded= (A * np.exp(1j*NewPhi))   
coded=roundcom(coded)
ang=np.angle(coded)
#print(ang[0,-msgbinlen+segmid:segmid])
codedwav=np.real(ifft(coded))
datanew=np.ravel(codedwav)

#Create the output wav file
outfile="_stego.wav"
write(audiofile+outfile,fs,np.array(datanew,dtype=np.float32))

#Ploting the signal
fig, axs = plt.subplots(1,2)
fig.tight_layout()
fig.set_size_inches(18, 5)
axs[0].plot(np.arange(0,len(data[0:segnum*seglen])),data[0:segnum*seglen],color='b')
axs[0].set_title(audiofile+".wav")
axs[1].plot(np.arange(0,len(data[0:segnum*seglen])),datanew,color='r')
axs[1].set_title(audiofile+outfile)
plt.savefig("Text_Stuff/Compare.png", dpi = 100)
plt.show()






print("Phase encoding Complete !!!\n",len(msg),"characters in",outfile)

