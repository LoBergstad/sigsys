import numpy as np
from scipy import signal

f_s = 24000
g_stop = 10 # Minsta dB reduktionen i stoppbandet
parameters = signal.cheb1ord(8000, 11000, 3, g_stop, analog = True)    
print(parameters)

