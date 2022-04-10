from matplotlib.pyplot import imread,imsave, imshow
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss
from scipy.io.wavfile import read,write

#Load audio
audiofile ="Photo_Stuff/ImageStego.wav"
audiofilenoise ="Photo_Stuff/ImageStegonoise.wav"
fs , data = read(audiofile)

#get height and width
height=data[-2]
width=data[-1]

bitsize=int(height)*int(width)*8*3

bitimage=[]

for i in range(bitsize):
    bitimage.append(data[i]%2)


imagebit=np.array(bitimage)
image1D=np.packbits(imagebit)
image2D=np.reshape(image1D,(height,width,3))

Output="Photo_Stuff/ImageOutput.jpg"
Outputnoise="Photo_Stuff/ImageOutputnoise.jpg"
imsave(Output,image2D)


print("Decode Complete !!!")