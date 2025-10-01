import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import control as ct

# --- System builder ---
def make_systems(GRC, R2R3):
    num3 = np.array([-1, 0, 0])      # -s**2
    num2 = np.array([-GRC, 0])       # -G/(RC)*s #Kommentaren och koden är inte samma uttryck (eller?)?
    num1 = np.array([-GRC**2])       # -(G/(RC))**2 #Kommentaren och koden är inte samma uttryck (eller?)?
    den  = np.array([1, R2R3*GRC, GRC**2])
    H3 = ct.tf(num3, den)
    H2 = ct.tf(num2, den)
    H1 = ct.tf(num1, den)
    return [H1, H2, H3]


# --- Initial constants ---
GRC0 = 2000
R2R3_0 = 1
systems = make_systems(GRC0, R2R3_0)
labels = ["H1", "H2", "H3"]

# --- Create big figure with subplots ---
fig, axes = plt.subplots(3, 3, figsize=(15, 12))
plt.subplots_adjust(bottom=0.25)  # leave space for sliders

# storage for artists (so we can update later)
pz_points = []
imp_lines = []
bode_mag_lines = []
bode_phase_lines = []

for row, (sys, label) in enumerate(zip(systems, labels)):
    # --- Pole-Zero Plot ---
    poles = ct.poles(sys)
    zeros = ct.zeros(sys)
    ax = axes[row, 0]
    pol_plot = ax.scatter(np.real(poles), np.imag(poles), marker='x', color='r', label="Poles")
    zer_plot = ax.scatter(np.real(zeros), np.imag(zeros), marker='o', facecolors='none', edgecolors='b', label="Zeros")
    pz_points.append((pol_plot, zer_plot))
    ax.set_xlabel("Real")
    ax.set_ylabel("Imag")
    ax.set_title(f"{label} Pole-Zero")
    ax.grid(True, which="both")
    ax.legend()

    # --- Impulse Response ---
    t, y = ct.impulse_response(sys)
    ax = axes[row, 1]
    line_imp, = ax.plot(t, y, 'b')
    imp_lines.append(line_imp)
    ax.set_xlabel("Time")
    ax.set_ylabel("Output")
    ax.set_title(f"{label} Impulse Response")
    ax.grid(True, which="both")
    #ax.set_xlim([0, 0.01])     # ev om vi vill ha fast skala (ändra)
    #ax.set_ylim([-1, 1])       # ev om vi vill ha fast skala (ändra)

    # --- Bode Plot ---
    mag, phase, omega = ct.bode(sys, plot=False)
    ax = axes[row, 2]
    ax2 = ax.twinx()
    line_mag, = ax.semilogx(omega, 20*np.log10(mag), 'b')
    line_phase, = ax2.semilogx(omega, phase*180/np.pi, 'r')
    bode_mag_lines.append(line_mag)
    bode_phase_lines.append(line_phase)
    ax.set_xlabel("ω [rad/s]")
    ax.set_ylabel("Mag [dB]", color='b')
    ax.tick_params(axis='y', labelcolor='b')
    ax.grid(True, which="both", ls="--")
    ax2.set_ylabel("Phase [deg]", color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax.set_title(f"{label} Bode")


# --- Sliders ---
axcolor = 'lightgoldenrodyellow'
axGRC = plt.axes([0.15, 0.12, 0.65, 0.03], facecolor=axcolor)
axR2R3 = plt.axes([0.15, 0.06, 0.65, 0.03], facecolor=axcolor)

sGRC = Slider(axGRC, 'G/(RC)', 100, 5000, valinit=GRC0)
sR2R3 = Slider(axR2R3, 'R2/R3', 0.1, 2.0, valinit=R2R3_0)


# --- Update function ---
def update(val):
    GRC = sGRC.val
    R2R3 = sR2R3.val
    systems = make_systems(GRC, R2R3)

    for row, sys in enumerate(systems):
        # Update pole-zero
        poles = ct.poles(sys)
        zeros = ct.zeros(sys)
        pz_points[row][0].set_offsets(np.c_[np.real(poles), np.imag(poles)])
        pz_points[row][1].set_offsets(np.c_[np.real(zeros), np.imag(zeros)])

        # Update impulse response
        t, y = ct.impulse_response(sys)
        imp_lines[row].set_xdata(t)
        imp_lines[row].set_ydata(y)

        # Update bode
        mag, phase, omega = ct.bode(sys, plot=False)
        bode_mag_lines[row].set_xdata(omega)
        bode_mag_lines[row].set_ydata(20*np.log10(mag))
        bode_phase_lines[row].set_xdata(omega)
        bode_phase_lines[row].set_ydata(phase*180/np.pi)

        # Autoscale för varje subplot
        axes[row,0].relim(); axes[row,0].autoscale()   # pole-zero
        axes[row,1].relim(); axes[row,1].autoscale()   # impulse
        axes[row,2].relim(); axes[row,2].autoscale()   # bode magnitude
        # axes[row,2].right_ax = axes[row,2].twinx()     # om du vill autoskala phase också
        # men bättre: spara ax2 i en lista och köra relim/autoscale på den också


    fig.canvas.draw_idle()


sGRC.on_changed(update)
sR2R3.on_changed(update)

plt.tight_layout(rect=[0, 0.15, 1, 1])  # keep space for sliders
plt.show()
