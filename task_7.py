import numpy as np
import matplotlib.pyplot as plt
import control as ct
from scipy import signal

# Constants
GRC = 1930  # 2000
R2R3 = 0.32 #0.3

# Numerator and denominator
num1 = np.array([-GRC**2])       # -(G/(RC))**2
den  = np.array([1, R2R3*GRC, GRC**2])

# Transfer functions
H1 = ct.tf(num1, den)

# --- Time vector ---
f = 100              # frequency in Hz
T_end = 0.04         # simulate 40 ms (4 period of 100 Hz)
dt = 1e-5            # timestep 10 µs
t = np.arange(0, T_end, dt)

# --- Square wave input ---
u = signal.square(2 * np.pi * f * t)   # values: -1 or +1

# --- Simulate response ---
t_out, y = ct.forced_response(H1, T=t, U=u)

# --- Plot ---
plt.figure(figsize=(10,4))
plt.plot(t*1000, u, 'black', label="Input signal x(t)")
plt.plot(t_out*1000, y, 'b', label="Output signal y1(t)")
plt.xlabel("Time [ms]")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.show()

"""Förklaring av resultaet:
Insignalen är en fyrkantsvåg. Vårat lågpassfilter filtrera bort dom höga frekvenserna dvs de svaga termerna i Fourierserien.
"Första toppen" blir högre pga (resonans) toppen i vårt LP-filter"""