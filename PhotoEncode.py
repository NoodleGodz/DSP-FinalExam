from matplotlib.pyplot import imread,imsave, imshow
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from scipy.io.wavfile import read,write

#Load audio
audiofile ="Photo_Stuff/MusicLong.wav"
fs , data = read(audiofile)

#if that is a stereo file, take right channel
if np.ndim(data)==2:
    data=data[:,1]


""" 
#plot the audio 
plt.plot(np.arange(len(data)),data)
plt.show()
"""

#load the image (only .jpg now) 
imagefile="Photo_Stuff/Green.jpg"
wm = imread(imagefile)
size=np.shape(wm)
bitsize=size[0]*size[1]*8*3


if bitsize>len(data):
    print("Image file is too large for the audio file")
    exit()

#Convert image to bit array [0 1]
bitimage=np.unpackbits(wm)


#Stego the bit to the data
datanew=data
for i in range(bitsize):
    if datanew[i] % 2 != bitimage[i]:
        datanew[i]+=1

#add row and columm of the image to the end of the signal
datanew[-2]=size[0]
datanew[-1]=size[1]

write("Photo_Stuff/ImageStego.wav",fs,np.array(datanew,dtype=data.dtype))

print("Encode Complete !!!")