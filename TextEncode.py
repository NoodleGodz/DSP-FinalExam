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
def inttofloat32(a:np.ndarray):
    data=np.iinfo(a.dtype)
    khoang=2
    khoangchia=data.max-data.min
    print(khoang)
    print(khoangchia)
    k=khoang/khoangchia
    v=[i*k for i in a]
    v=np.array(v,np.float32)
    return v


#Load audio
audiofile ="MusicLong"
fs , data = read(audiofile+".wav")
print(data.dtype)
if data.dtype!=np.float32:
    data=inttofloat32(data)

#if that is a stereo file, take right channel
if np.ndim(data)==2:
    data=data[:,1]

textfile='texttostego.txt'
txt=open(textfile,'r')
msg=txt.read()
txt.close()

msgbin = np.ravel([[int(y) for y in format(ord(x), '08b')] for x in msg])
msgbinlen=len(msgbin)
#print(bintotext(msgbin))


seglen = int(2**np.ceil(np.log2(2*msgbinlen)))
segnum = int(np.floor(len(data)/seglen))
print(seglen * segnum <= len(data))


msgPhi = msgbin.copy()
msgPhi[msgPhi == 0] = -1
msgPhi = msgPhi * -(np.pi/2)



segments = data[0:segnum*seglen].reshape((segnum,seglen))
fsegments = fft(segments)
fsegments = roundcom(fsegments)
A = np.absolute(fsegments)
Phi = np.angle(fsegments)
NewPhi=Phi.copy()



DeltaPhi=np.diff(Phi,axis=0)


segmid = seglen // 2
NewPhi[0,-msgbinlen+segmid:segmid] = msgPhi
NewPhi[0,segmid+1:segmid+1+msgbinlen] = -msgPhi[::-1]

print(segnum," ",seglen)

for i in range(1, segnum): 
    NewPhi[i,:] = NewPhi[i-1,:] + DeltaPhi[i-1,:]

"""
d=NewPhi[0,-msgbinlen+segmid:segmid]/-(np.pi/2)
d[d==-1]=0
print(bintotext(d))
"""


coded= (A * np.exp(1j*NewPhi))   
coded=roundcom(coded)
ang=np.angle(coded)
#print(ang[0,-msgbinlen+segmid:segmid])
codedwav=np.real(ifft(coded))
datanew=np.ravel(codedwav)
print(datanew[0:50])
"""
vl=fft(codedwav)
vl=roundcom(vl)
vlm=np.absolute(vl)
vla=np.angle(vl)


print(vla[0,-msgbinlen+segmid:segmid])

"""
"""

"""
fig, axs = plt.subplots(1,2)
fig.tight_layout()
fig.set_size_inches(18, 5)
axs[0].plot(np.arange(0,len(data[0:segnum*seglen])),data[0:segnum*seglen],color='b')
axs[0].set_title(audiofile+".wav")
axs[1].plot(np.arange(0,len(data[0:segnum*seglen])),datanew,color='r')
axs[1].set_title("TextStego.wav")
plt.savefig("Compare.png", dpi = 100)
plt.show()
outfile="_stego.wav"
write(audiofile+outfile,fs,np.array(datanew,dtype=np.float32))

print("Phase Coding Complete !!!\n",len(msg),"characters in",outfile)

"""
test=datanew.reshape((segnum,seglen))
phitest=np.angle(roundcom(fft(test)))
phitest2 = phitest[0,-msgbinlen+segmid:segmid]
d=phitest2/-(np.pi/2)
d[d==-1]=0
print(bintotext(d))
"""