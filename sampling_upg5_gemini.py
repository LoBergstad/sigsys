import numpy as np
from scipy import signal, fft
import control as ct
import matplotlib.pyplot as plt

# --- 1. Filterdesign & Simulation ---

f_s = 24000 # Samplefrekvens
# Mål för dämpning: max 0.5/(2^11) V från 1 V störning
g_stop = 20*np.log10(0.5 / (2**11)) # Korrekt dämpningsmål i dB (ca -66.2 dB)

W_pass = 8000 * 2 * np.pi  # Passband (8 kHz)
W_stop = 11000 * 2 * np.pi # Stoppband (11 kHz)

# Beräkna filterordningen (deg) och nödvändig stoppbandskant (Wn)
deg, Wn_stop = signal.cheb1ord(W_pass, W_stop, 3, -g_stop, analog = True)

# Designa filtret: Använd PASSBANDETS frekvens (W_pass) som gränsfrekvens
numerator, denominator = signal.cheby1(deg, 3, W_pass, analog = True)
sys = signal.lti(numerator, denominator)

# Input signals
frequency_slow = 4*1e+3 # 4 kHz
frequency_fast = 11*1e+3  # 11 kHz
f_analog = f_s * 100 # Upplösning
# Tidsvektor: Mät exakt x perioder av den långsamma signalen och använd endpoint=False
perioder = 40
T_total = perioder / frequency_slow
time_vector = np.linspace(0, T_total, int(T_total * f_analog), endpoint=False)
sin_slow = np.sin(frequency_slow*2*np.pi*time_vector)
sin_fast = np.sin(frequency_fast*2*np.pi*time_vector)
x = sin_slow + sin_fast # Total insignal

# Filtrering och Sampling
t_out, y, _ = signal.lsim(sys, x, time_vector)

step = int(f_analog/f_s)
y_sample = y[::step]

# --- 2. Uppgift 5: DFT-analys ---

Y = fft.fft(y_sample)
N = len(y_sample)

# Skapa Frekvensaxel och välj positiv del
freqs = fft.fftfreq(N, d=1 / f_s)
pos_boolean = freqs >= 0
freqs_pos = freqs[pos_boolean]
Y_pos = Y[pos_boolean]

# Normalisering: Multiplicera med 2 / N
amplitude = 2 * np.abs(Y_pos) / N

# --- 3. Plotta Amplitudspektrum ---
plt.figure(figsize=(10, 6))
# Krav: Frekvensaxeln ska vara i kHz
plt.plot(freqs_pos / 1000, amplitude) 
plt.title("Amplitudspektrum för den Samplade Utsignalen (Normaliserad)")
plt.xlabel("Frekvens [kHz]") # Ändrad till kHz för att uppfylla kravet
plt.ylabel("Amplitud [Volt]")
plt.grid(True, which="both", ls="--")
plt.xlim(0, f_s/2/1000) # upp till Nyquist (12 kHz)
plt.show()

# --- Kontrollutskrift ---
# Hitta toppen vid 4 kHz för kontroll
target_freq_index_4k = np.argmin(np.abs(freqs_pos - 4000))
print(f"Filterordning: {deg}")
print(f"Topp vid 4 kHz: {amplitude[target_freq_index_4k]:.4f} V")