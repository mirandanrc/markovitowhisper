#!/usr/bin/env python3
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from pylab import*


samplerate, data = wavfile.read('/home/hp/pruebas/markovtest3.wav')
print(f"number of channels = {data.shape[1]}")
print(data.dtype)
length = data.shape[0] / samplerate
print(f"length = {length}s")
data2=abs(data)
promedio=np.mean(data2[1])
data2=data2[9000:]
time = np.linspace(0., length, data2.shape[0])
print("El promedio es: ",promedio)
# for c in range(1000):
#     if data2[c][1]>=0.2:
#         data2=np.delete(data2,c)
# plt.plot(time, data2[:, 0], label="Left channel")
plt.plot(time, data2[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()


# s1=data[:,0]
# n=len(s1)
# p=fft(s1)
# nUniquePts = int(np.ceil((n+1)/2.0))
# p = p[0:nUniquePts]
# p = abs(p)
# p = p / float(n)
# p = p**2
# if n % 2 > 0: # we've got odd number of points fft
#     p[1:len(p)] = p[1:len(p)] * 2
# else:
#     p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft

# freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / n)
# plt.plot(freqArray/1000, 10*np.log10(p), color='k')
# plt.xlabel('Frequency (kHz)')
# plt.ylabel('Power (dB)')
# plt.show()

