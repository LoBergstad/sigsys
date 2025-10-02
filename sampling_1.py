import numpy as np
from scipy import signal
import control as ct
import matplotlib.pyplot as plt

# --- Värden ---
f_s = 24000 #Samplefrekvens (hitte på över 16000 enligt Nyqvist)
g_stop = 10 # Minsta dB reduktionen i stoppbandet, hittar på 10


parameters = signal.cheb1ord(8000, 11000, 3, g_stop, analog = True) #Beräknar ordnignen som vi behöver på vårat chebichev filter
#print('Chebichev1-filter, ordning:', parameters[0])

#Behöver ordning 3, ger tillbaka frekvens 8000

numerator, denominator = signal.cheby1(3, 3, 8000, analog = True)
#print(filter)

sys = signal.lti(numerator, denominator)

w, mag, phase = signal.bode(sys)
freq_hz = w/(2*np.pi)

# Rita i samma bild
fig, ax1 = plt.subplots(figsize=(10, 5))

color1 = 'tab:red'
ax1.set_xlabel("Frekvens (Hz)")
ax1.set_ylabel("Magnitud (dB)", color=color1)
ax1.semilogx(freq_hz, mag, color=color1, label="Magnitud")
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, which="both", ls="--")

ax2 = ax1.twinx()  # dela x-axeln men ha egen y-axel
color2 = 'tab:blue'
ax2.set_ylabel("Fas (grader)", color=color2)
ax2.semilogx(freq_hz, phase, color=color2, label="Fas")
ax2.tick_params(axis='y', labelcolor=color2)

fig.tight_layout()
plt.title("Bode-diagram (Chebyshev I)")
plt.show()

