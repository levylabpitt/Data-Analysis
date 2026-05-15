# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:43:01 2026

@author: Ranjani

To get are under curve of S21 for each dc bias, for given freq range
"""

import skrf as rf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

################functions

def integrate_s21_range(freq, S21_dB, f_min, f_max, convert_to_linear=True):
    """
    Integrate S21 vs frequency over a given frequency range.

    Parameters:
        freq (array): frequency in Hz
        S21_dB (array): S21 in dB
        f_min (float): lower frequency bound (Hz)
        f_max (float): upper frequency bound (Hz)
        convert_to_linear (bool): convert dB → linear before integrating

    Returns:
        area (float): area under curve
    """

    # Mask for frequency range
    mask = (freq >= f_min) & (freq <= f_max)
    f_sel = freq[mask]
    S21_sel = S21_dB[mask]

    if len(f_sel) < 2:
        raise ValueError("Not enough points in selected frequency range.")

    # Convert dB → linear if needed
    if convert_to_linear:
        S21_sel = 10**(S21_sel / 20)

    # Numerical integration (trapezoidal rule)
    area = np.trapz(S21_sel, f_sel)

    return area



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

# Folder where your .S2P files are located
s2p_folder = '.'  # current folder; change if needed
plt.figure(figsize=(6,4))

# Half-width (Hz)
delf = 0.0003e9   # example: 0.5 GHz

# f0 list (Hz) — MUST match number/order of files
f0_list = [1.0888e9,1.0893e9,1.0888e9,1.0885e9,1.0885e9,1.0883e9,1.0883e9]

plt.figure(figsize=(6,4))

for i, filename in enumerate(sorted(os.listdir(s2p_folder))):
    if filename.lower().endswith('.s2p'):

        ntwk = rf.Network(os.path.join(s2p_folder, filename))
        
        S21_dB = 20 * np.log10(np.abs(ntwk.s[:, 0, 1]))
        freq = ntwk.f
        freq_GHz = freq

        # --- baseline subtraction ---
        n_baseline = min(10, len(S21_dB))
        baseline = np.mean(S21_dB[:n_baseline])
        S21_dB_corr = S21_dB - baseline
        #S21_dB_corr = S21_dB 

        # --- get f0 for this file ---
        f0 = f0_list[i]

        # define range
        f_min = f0 - delf
        f_max = f0 + delf

        # --- mask for range ---
        mask = (freq >= f_min) & (freq <= f_max)

        # --- plot ONLY that range ---
        plt.plot(freq_GHz[mask], S21_dB_corr[mask], label=filename)

        # --- integrate ---
        area = integrate_s21_range(freq, S21_dB_corr, f_min, f_max)

        print(f"{filename}: f0={f0/1e9:.6f} GHz, Area={area:.3e}")
        
plt.xlabel("Frequency (GHz)")
plt.ylabel("S21 (dB, baseline subtracted)")
plt.title("S21 around f0")
plt.legend(fontsize=6)
plt.grid(True)

plt.tight_layout()
plt.show()

# Loop through all .S2P files in the folder
# for filename in os.listdir(s2p_folder):
#     if filename.lower().endswith('.s2p'):
#         # Load the network
#         ntwk = rf.Network(os.path.join(s2p_folder, filename))
        
#         # Calculate S21 in dB
#         S21_dB = 20 * np.log10(np.abs(ntwk.s[:, 0, 1]))

#         freq = ntwk.f
#         # Find maximum S21_dB value
#         max_S21_dB = np.max(S21_dB)
        
#         # Print result
#         #print(f"{filename}: Max S21_dB = {max_S21_dB:.2f} dB")
      
#         # Define your frequency range (Hz)
#         f_min = 1.0885e9   # example: 1 GHz
#         f_max = 1.0887e9   # example: 5 GHz
#         # Baseline = average of first 10 points
#         baseline = np.mean(S21_dB[:10])

#         # Subtract baseline
#         S21_dB = S21_dB - baseline
#         #S21_dB = S21_dB + 60 #baseline shift
#         area = integrate_s21_range(freq, S21_dB, f_min, f_max)

#         print(f"{filename}: Area (S21 vs f) = {area:.3e}")
        
#         freq_GHz = freq / 1e9

#         plt.plot(freq_GHz, S21_dB, label=filename)

# plt.xlabel("Frequency (GHz)")
# plt.ylabel("S21 (dB)")
# plt.title("S21 vs Frequency")
# plt.xlim(f_min/1e9, f_max/1e9)
# plt.legend(fontsize=8)
# plt.grid(True)

# plt.tight_layout()
# plt.show()