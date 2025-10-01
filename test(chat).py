import numpy as np
import matplotlib.pyplot as plt
import control as ct

# Constants
G = R = C = R2 = R3 = 1
GRC = G / (R * C)
R2R3 = R2 / R3

GRC = 2000  # 2000
R2R3 = 2  #0.3

# Numerators and denominator
num3 = np.array([-1, 0, 0])      # -s**2
num2 = np.array([-GRC, 0])       # -G/(RC)*s
num1 = np.array([-GRC**2])       # -(G/(RC))**2
den  = np.array([1, R2R3*GRC, GRC**2])

# Transfer functions
H3 = ct.tf(num3, den)
H2 = ct.tf(num2, den)
H1 = ct.tf(num1, den)

systems = [H1, H2, H3]
labels = ["H1", "H2", "H3"]

# Create big figure with 3x3 subplots
fig, axes = plt.subplots(3, 3, figsize=(15, 12))

for row, (sys, label) in enumerate(zip(systems, labels)):
    # --- Pole-Zero Plot ---
    poles = ct.poles(sys)
    zeros = ct.zeros(sys)
    ax = axes[row, 0]
    ax.scatter(np.real(poles), np.imag(poles), marker='x', color='r', label="Poles")
    ax.scatter(np.real(zeros), np.imag(zeros), marker='o', facecolors = None, edgecolors='b', label="Zeros")
    ax.set_xlabel("Real")
    ax.set_ylabel("Imag")
    ax.set_title(f"{label} Pole-Zero")
    ax.set_xlim(np.min(np.real(poles))*1.1, -0.1*np.min(np.real(poles)))
    ax.grid(True, which="both")
    ax.legend()

    # --- Impulse Response ---
    t, y = ct.impulse_response(sys)
    ax = axes[row, 1]
    ax.plot(t, y, 'b')  
    ax.set_xlabel("Time")
    ax.set_ylabel("Output")
    ax.set_title(f"{label} Impulse Response")
    ax.grid(True, which="both")

    # --- Bode Plot ---
    mag, phase, omega = ct.frequency_response(sys)
    ax = axes[row, 2]
    ax2 = ax.twinx()
    ax.semilogx(omega, 20*np.log10(mag), 'b')
    ax.set_xlabel("ω [rad/s]")
    ax.set_ylabel("Mag [dB]", color='b')
    ax.tick_params(axis='y', labelcolor='b')
    ax2.set_ylim(-190, 190)
    ax.grid(True, which="both", ls="--")
    ax2.semilogx(omega, phase*180/np.pi, 'r')
    ax2.set_ylabel("Phase [deg]", color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax.set_title(f"{label} Bode")

fig.suptitle(f'R2/R3 = {R2R3}, G/RC = {GRC}', color = 'r', fontsize = 14)
plt.tight_layout(rect=[0, 0, 1, 0.99])
plt.show() 

