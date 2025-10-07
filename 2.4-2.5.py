import numpy as np
from scipy import signal, fft
import control as ct
import matplotlib.pyplot as plt

# --- Värden ---
f_s = 24000 #Samplefrekvens (hitte på över 16000 enligt Nyqvist)
g_stop = 20*np.log10(2**(-12)) # Minsta dB reduktionen i stoppbandet, får fluktuera max 2**(-12) från noll, för om till dB

W_pass = 8000 * 2 * np.pi  # Passband (8 kHz)
W_stop = 11000 * 2 * np.pi # Stoppband (11 kHz)

deg, stop_frequency = signal.cheb1ord(W_pass, W_stop, 3, -g_stop, analog = True) #Beräknar ordnignen som vi behöver på vårat chebychev filter

numerator, denominator = signal.cheby1(deg, 3, stop_frequency, analog = True)   # Täljare och nämnare för överföringsfunktionen

sys = signal.lti(numerator, denominator)    # Skapar ett systemobjekt för filtret

# Input signals
frequency_slow = 4*1e+3 # Frekvens för riktiga signalen
frequency_fast = 11*1e+3    #Frekvens för brussignalen
f_analog = f_s*100 # Upplösning på 100ggr sample rate, modell av analog signal

#Tidsvektor och grejer
periods = 4 #Antal perioder
T_total = periods / frequency_slow
time_vector = np.linspace(0, T_total, int(T_total * f_analog))  # Tidsvektor för den långsamma signalen
sin_slow = np.sin(frequency_slow*2*np.pi*time_vector)   # Riktiga signalen
sin_fast = np.sin(frequency_fast*2*np.pi*time_vector)  # Pålagt brus
x = sin_slow + sin_fast     # Total insignal

t_out, y, _ = signal.lsim(sys, x, time_vector) # Tidsvektor och analog utsignal

time_vector_sample = t_out[0::int(f_analog/f_s)]    # Samplad tidsvektor, tar var 100e värde från den "analoga" tidsvektorn
y_sample = y[0::int(f_analog/f_s)]                  # Samplad utsignal, -//-



# Plotta insignal(er) och utsignal
plt.plot(time_vector, x, label = 'x(t)')    # "Analog" insignal
#plt.plot(time_vector, sin_slow, label = 'Slow Sine')    # "Analog", riktiga signalen
#plt.plot(time_vector, sin_fast, label = 'Fast Sine')    # "Analog", brussignalen
plt.plot(time_vector, y, label = 'y(t) (ej filtrerad)')   # Samplad utsignal
plt.scatter(time_vector_sample, y_sample, label = 'y(t)')   # Samplad utsignal
plt.legend()
#plt.show()




Y = fft.fft(y_sample)                  # Filtrerad signal
#Y = fft.fft(x[0::int(f_analog/f_s)])    # Ej filtrerad signal
N = len(Y)
freqs = fft.fftfreq(N, d=1 / f_s)
# Endast positiva frekvenser
pos_boolean = freqs >= 0
freqs_pos = freqs[pos_boolean]
Y_pos = Y[pos_boolean]


# Amplitudspektrum (enkel-sidig) och normalisering (*2/N)
amplitude = np.abs(Y_pos) * 2 / N

# --- Plotta amplitudspektrum ---
plt.figure(figsize=(8, 4))
plt.plot(freqs_pos / 1000, amplitude) # /1000 för att få i kHz
plt.title("Amplitude Spectrum of Filtered Output")
plt.xlabel("Frequency [kHz]")
plt.ylabel("Amplitude")
plt.grid(True, which="both", ls="--")
plt.xlim(0, f_s/2/1000)  # upp till Nyquist
plt.show()

