import numpy as np
from scipy import signal
import control as ct
import matplotlib.pyplot as plt

# --- Värden ---
f_s = 24000 #Samplefrekvens (hitte på över 16000 enligt Nyqvist)
g_stop = 20*np.log10(2**(-12)) # Minsta dB reduktionen i stoppbandet, hittar på 10


deg, stop_frequency = signal.cheb1ord(8000, 11000, 3, -g_stop, analog = True) #Beräknar ordnignen som vi behöver på vårat chebichev filter
#print('Chebichev1-filter, ordning:', deg)

#Behöver ordning 3, ger tillbaka frekvens 8000

numerator, denominator = signal.cheby1(deg, 3, 8000, analog = True)
#print(filter)

sys = signal.lti(numerator, denominator)

n = 10**5   #Antal omega för boden
w_faster = np.linspace(1e+1, 1e+5, n)  #Flera w punkter
w, mag, phase = signal.bode(sys, w_faster)
freq_hz = w/(2*np.pi)


# Input signals
frequency_slow = 4*1e+3
frequency_fast = 40*1e+3
f_analog = 24*10**5 # Upplösning på 100ggr sample rate
time_vector = np.linspace(0, 4/frequency_slow, f_analog)  
time_vector_sample = time_vector[0::int(f_analog/f_s)]
sin_slow = np.sin(frequency_slow*2*np.pi*time_vector)   # Riktiga signalen, 4 perioder
sin_slow_sample = sin_slow[0::int(f_analog/f_s)]
sin_fast =  np.sin(frequency_fast*2*np.pi*time_vector)  # Pålagt brus
sin_fast_sample = sin_fast[0::int(f_analog/f_s)]


#plt.plot(time_vector, sin_slow)
plt.scatter(time_vector_sample, sin_slow_sample + sin_fast_sample)

plt.show()

