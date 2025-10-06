import numpy as np
from scipy import signal
import control as ct
import matplotlib.pyplot as plt

# --- Värden ---
f_s = 24000 #Samplefrekvens (hitte på över 16000 enligt Nyqvist)
g_stop = 20*np.log10(2**(-12)) # Minsta dB reduktionen i stoppbandet, får fluktuera max 2**(-12) från noll, för om till dB


deg, stop_frequency = signal.cheb1ord(8000*2*np.pi, 11000*np.pi, 3, -g_stop, analog = True) #Beräknar ordnignen som vi behöver på vårat chebychev filter

numerator, denominator = signal.cheby1(deg, 3, stop_frequency, analog = True)   # Täljare och nämnare för överföringsfunktionen

sys = signal.lti(numerator, denominator)    # Skapar ett systemobjekt för filtret

# Input signals
frequency_slow = 4*1e+3 # Frekvens för riktiga signalen
frequency_fast = 20*1e+3    #Frekvens för brussignalen
f_analog = f_s*100 # Upplösning på 100ggr sample rate, modell av analog signal
time_vector = np.linspace(0, 4/frequency_slow, f_analog)  # Tidsvektor för fyra perioder av den långsamma signalen
sin_slow = np.sin(frequency_slow*2*np.pi*time_vector)   # Riktiga signalen, 4 perioder
sin_fast =  np.sin(frequency_fast*2*np.pi*time_vector)  # Pålagt brus
x = sin_slow + sin_fast     # Total insignal

t_out, y, _ = signal.lsim(sys, x, time_vector) # Tidsvektor och analog utsignal

time_vector_sample = t_out[0::int(f_analog/f_s)]    # Samplad tidsvektor, tar var 100e värde från den "analoga" tidsvektorn
y_sample = y[0::int(f_analog/f_s)]                  # Samplad utsignal, -//-



# Plotta insignal(er) och utsignal
plt.plot(time_vector, x, label = 'x(t)')    # "Analog" insignal
#plt.plot(time_vector, sin_slow, label = 'Slow Sine')    # "Analog", riktiga signalen
#plt.plot(time_vector, sin_fast, label = 'Fast Sine')    # "Analog", brussignalen
plt.scatter(time_vector_sample, y_sample, label = 'y(t)')   # Samplad utsignal
plt.legend()
plt.show()



