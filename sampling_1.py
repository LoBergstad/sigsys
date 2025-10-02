import numpy as np
from scipy import signal

f_s = 24000
g_stop = 10 # Minsta dB reduktionen i stoppbandet, hittar på 10
parameters = signal.cheb1ord(8000, 11000, 3, g_stop, analog = True)    
print(parameters)

# Behöver ordning 3, ger tillbaka frekvens 8000

filter = signal.cheby1(3, 3)