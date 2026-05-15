# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 10:41:39 2025

@author: ramachandran
"""
import skrf as rf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

################functions
#To plot polar of S12
def plot_s12_polar(s2p_filename):
    # Load network
    ntwk = rf.Network(s2p_filename)

    # Extract frequency, magnitude and phase of S12
    freq = ntwk.f / 1e9  # GHz
    S12 = ntwk.s[:, 1, 0]
    mag = np.abs(S12)
    phase = np.angle(S12)  # radians

    # Create polar plot
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(7, 7))
    # Reduce radial label count
    ax.set_yticks([0.01, 0.02])

   # Plot line connecting all points (in order of frequency)
    ax.plot(phase, mag, color='gray', linewidth=1.0, alpha=0.5)

    # Create scatter with color mapped to frequency
    c = ax.scatter(phase, mag, c=freq, cmap='viridis', s=10, vmin=1.08, vmax=1.095)
    #ax.set_rlim(0, 0.025)


    # Add colorbar
    cb = plt.colorbar(c, ax=ax, pad=0.1)
    cb.set_label('Frequency (GHz)')

    ax.set_title('S12 Polar Plot')
    plt.tight_layout()
    plt.show()
    
#To plot s12 phase vd freq
def plot_s12_phase(s2p_filename):
    """
    Plot the phase of S12 vs frequency (GHz) from a .s2p file.
    """
    # Load the network
    ntwk = rf.Network(s2p_filename)

    # Frequency in GHz
    freq_ghz = ntwk.f / 1e9

    # Extract S12 phase in degrees
    S12 = ntwk.s[:, 1, 0]
    phase_deg = np.unwrap(np.angle(S12))

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(freq_ghz, phase_deg, label='∠S12 (radian)')
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Phase (radians)')
    plt.title('S12 Phase vs Frequency')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

#Save all 4 sparms as itx file for igor
def save_sparams_to_itx(x_array, y_arrays, output_filename, s2p_filename, 
                        x_label="f", y_labels=None, x_unit="(GHz)", y_unit="(dB)"):
    """
    Save x data and 4 S-parameter dB arrays into an IGOR-compatible .itx file.

    Parameters:
    - x_array (array-like): X-axis data (e.g., frequency in GHz)
    - y_arrays (list of array-like): [S11_dB, S21_dB, S12_dB, S22_dB]
    - output_filename (str): Base filename for output .itx file (no extension)
    - s2p_filename (str): Original .s2p file name (for metadata)
    - x_label (str): Label for x-axis
    - y_labels (list of str): Custom y wave names (default: ['S11', 'S21', 'S12', 'S22'])
    - x_unit (str): Unit for x-axis
    - y_unit (str): Unit for y-axis
    """
    if not isinstance(y_arrays, list) or len(y_arrays) != 4:
        raise ValueError("y_arrays must be a list of 4 arrays: [S11_dB, S21_dB, S12_dB, S22_dB]")
    
    N = len(x_array)
    for y in y_arrays:
        if len(y) != N:
            raise ValueError("All y arrays must have the same length as x_array.")
    
    if y_labels is None:
        y_labels = ['S11', 'S21', 'S12', 'S22']
    
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p").lstrip("0").replace("/0", "/")
    s2p_base = os.path.basename(s2p_filename)

    content = f"""IGOR
X// Date: {now}
X// Source: {s2p_base}
"""

    # X wave
    xwave = f"x{output_filename}"
    content += f"WAVES/D/N=({N}) '{xwave}'\nBEGIN\n"
    content += "\n".join([f"{val:.15E}" for val in x_array]) + "\nEND\n\n"

    # Y waves (now in order S11, S21, S12, S22)
    ywaves = []
    for i in range(4):
        ywave = f"y{output_filename}_{y_labels[i]}"
        ywaves.append(ywave)
        content += f"WAVES/D/N=({N}) '{ywave}'\nBEGIN\n"
        content += "\n".join([f"{val:.15E}" for val in y_arrays[i]]) + "\nEND\n\n"

    # Plotting
    content += "X Display\n"
    content += f"X AppendToGraph '{ywaves[0]}' vs '{xwave}'\n"
    for ywave in ywaves[1:]:
        content += f"X AppendToGraph '{ywave}' vs '{xwave}'\n"

    content += f"""X ModifyGraph height=172
X ModifyGraph Log(bottom)=0
X ModifyGraph Log(left)=0
X ModifyGraph mirror=1
X ModifyGraph width=216
X Label bottom "{x_label} {x_unit}"
X Label left "{y_labels[0]} {y_unit}"
"""

    with open(f"{output_filename}.itx", "w") as f:
        f.write(content)

    print(f"Saved: {output_filename}.itx (from {s2p_base})")

########################################
# Save all S parms in itx file

s2p_file = "D3cd-30-25V_250716-009.S2P"
ntwk = rf.Network(s2p_file)
freq = ntwk.f / 1e9  # GHz

# Reordered: S11, S21, S12, S22
S11_dB = 20 * np.log10(np.abs(ntwk.s[:, 0, 0]))
S21_dB = 20 * np.log10(np.abs(ntwk.s[:, 0, 1]))
S12_dB = 20 * np.log10(np.abs(ntwk.s[:, 1, 0]))
S22_dB = 20 * np.log10(np.abs(ntwk.s[:, 1, 1]))

save_sparams_to_itx(freq, [S11_dB, S21_dB, S12_dB, S22_dB], output_filename="D3cd25V", s2p_filename=s2p_file)







###############################
# #Just plotting Sparms 
# #Load S-parameter data
# ntwk = rf.Network('D3bc-30-30V_250716-002.s2p')  # Replace with your filename

# # Frequency in GHz
# freq = ntwk.f / 1e9

#Get S12 (port 1 ← port 0)
# S12 = ntwk.s[:, 0, 1]


# # Plot S12 magnitude in dB
# plt.figure(figsize=(8,5))
# plt.plot(freq, 20 * np.log10(np.abs(S12)), label='|S12| (dB)')
# plt.xlabel('Frequency (GHz)')
# plt.ylabel('Magnitude (dB)')
# plt.title('S12 Magnitude vs Frequency')
# plt.grid(True)
# plt.legend()

# # Remove empty space on x-axis
# plt.xlim(freq.min(), freq.max())

# plt.tight_layout()
# plt.show()

####################
## Just calling S12 polar and S12 phase
#plot_s12_phase('D3cd-30-30V_250716-010.s2p')

