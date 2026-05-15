# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 13:32:51 2025
Saves s1p to itx
@author: Ranjani
"""

import skrf as rf
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from scipy.signal import find_peaks

# Your save function from before, adjusted to linear magnitude (y_unit)
# --- Save to IGOR .itx file ---
def save_s1p_to_itx(x_array, y_array, output_filename, s1p_filename, 
                    x_label="t", y_label="S21", x_unit="(s)", y_unit="(dB)"):
    if len(x_array) != len(y_array):
        raise ValueError("x_array and y_array must have the same length.")

    now = datetime.now().strftime("%m/%d/%Y %I:%M %p").lstrip("0").replace("/0", "/")
    s1p_base = os.path.basename(s1p_filename)

    content = f"""IGOR
X// Date: {now}
X// Source: {s1p_base}
"""

    xwave = f"x{output_filename}"
    ywave = f"y{output_filename}_{y_label}"

    content += f"WAVES/D/N=({len(x_array)}) '{xwave}'\nBEGIN\n"
    content += "\n".join([f"{val:.15E}" for val in x_array]) + "\nEND\n\n"

    content += f"WAVES/D/N=({len(y_array)}) '{ywave}'\nBEGIN\n"
    content += "\n".join([f"{val:.15E}" for val in y_array]) + "\nEND\n\n"

    content += "X Display\n"
    content += f"X AppendToGraph '{ywave}' vs '{xwave}'\n"
    content += f"""X ModifyGraph height=172
X ModifyGraph Log(bottom)=0
X ModifyGraph Log(left)=0
X ModifyGraph mirror=1
X ModifyGraph width=216
X Label bottom "{x_label} {x_unit}"
X Label left "{y_label} {y_unit}"
"""

    with open(f"{output_filename}.itx", "w") as f:
        f.write(content)

    print(f"Saved: {output_filename}.itx (from {s1p_base})")


######################################################
# --- Load .s1p and extract S21 (dB) ---
s1p_file = "23m-250716-015.S1P"  # ← Replace with your actual file
ntwk = rf.Network(s1p_file)

time = ntwk.f   # Frequency in GHz
s21_complex = ntwk.s[:, 0, 0]  # S21 complex
s21_dB = 20 * np.log10(np.abs(s21_complex))  # S21 magnitude in dB
s21_mag = np.abs(ntwk.s[:, 0, 0])  # S21 without converting to dB, jst magnitude

# --- Plot S21 (dB) vs frequency ---
plt.figure()
plt.plot(time, s21_dB)
plt.xlabel("time (s)")
plt.ylabel("S21 Magnitude (dB)")
plt.title("S21 (dB) vs time")
plt.grid(True)
plt.show()

# --- Save to IGOR .itx ---
save_s1p_to_itx(time, s21_dB, "D3cd_23min", s1p_file,
                x_label="f", y_label="S21",x_unit="(Hz)", y_unit="(dB)")


# # --- Subtract baseline ---
# baseline = -80 - 40e6 * time
# s21_corrected = s21_dB - baseline

# # --- Find local maxima ---
# max_indices, _ = find_peaks(s21_dB,prominence=0.00000000001)  # find maxima by finding peaks in -S21_dB
# max_times = time[max_indices]
# max_values = s21_dB[max_indices]

# # --- Print or use the results ---
# for t, val in zip(max_times, max_values):
#     print(f"maximum at time = {t:.6g}, S21_dB = {val:.2f} dB")

# # Optional: plot to visualize

# plt.figure()
# plt.plot(time, s21_dB, label="S21 (dB)")
# plt.plot(max_times, max_values, 'ro', label="maxima")
# plt.xlabel("Time (µs)")
# plt.ylabel("S21 (dB)")
# plt.title("S21 vs Time with Local maxima")
# plt.legend()
# plt.grid(True)
# plt.show()

# # --- Save to IGOR .itx ---
# save_s1p_to_itx(max_times, max_values, "D3bctimepeaks", s1p_file,
#                 x_label="t", y_label="S21",x_unit="(s)", y_unit="(dB)")