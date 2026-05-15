# -*- coding: utf-8 -*-
"""
Created on Wed Aug  6 15:23:44 2025

@author: Ranjani
"""
import skrf as rf
import numpy as np
import os
import re
from datetime import datetime
import matplotlib.pyplot as plt

def save_max_s11_to_itx(x_array, y_array, output_filename, comment_label="S11 max vs time"):
    now = datetime.now().strftime("%m/%d/%Y %I:%M %p").lstrip("0").replace("/0", "/")

    content = f"""IGOR
X// Date: {now}
X// Comment: {comment_label}
"""

    N = len(x_array)

    # X wave: time in minutes
    content += f"WAVES/D/N=({N}) xMinutes\nBEGIN\n"
    content += "\n".join([f"{x:.15E}" for x in x_array]) + "\nEND\n\n"

    # Y wave: max S11 in dB
    content += f"WAVES/D/N=({N}) yMaxS11_dB\nBEGIN\n"
    content += "\n".join([f"{y:.15E}" for y in y_array]) + "\nEND\n\n"

    content += f"""X Display
X AppendToGraph yMaxS11_dB vs xMinutes
X ModifyGraph height=172
X ModifyGraph Log(bottom)=0
X ModifyGraph Log(left)=0
X ModifyGraph mirror=1
X ModifyGraph width=216
X Label bottom "Time (minutes)"
X Label left "Max S11 (dB)"
"""

    with open(output_filename, "w") as f:
        f.write(content)

    print(f"Saved ITX file: {output_filename}")


### Main analysis

s1p_folder = '.'  # current directory

# Matches either '12m30s' or '12m'
pattern_full = re.compile(r'(\d+)m(\d+)s')
pattern_min_only = re.compile(r'(\d+)m(?!\d*s)')  # 12m with no seconds

x_minutes = []
y_max_s11_dB = []

for filename in os.listdir(s1p_folder):
    if filename.lower().endswith('.s1p'):
        minutes = None
        seconds = 0

        if (match := pattern_full.search(filename)):
            minutes = int(match.group(1))
            seconds = int(match.group(2))
        elif (match := pattern_min_only.search(filename)):
            minutes = int(match.group(1))

        if minutes is not None:
            total_minutes = minutes + seconds / 60.0

            # Load .s1p and get max S11
            ntwk = rf.Network(os.path.join(s1p_folder, filename))
            S11_dB = 20 * np.log10(np.abs(ntwk.s[:, 0, 0]))
            max_S11_dB = np.max(S11_dB)
            # # Frequency in GHz
            freq = ntwk.f / 1e9
            
            # Plot S11 for this time
            plt.plot(freq, S11_dB, linestyle=':', linewidth=0.5, label=f"{total_minutes:.2f} min")
            
            x_minutes.append(total_minutes)
            y_max_s11_dB.append(max_S11_dB)
            
            print(f"{filename}: Time = {total_minutes:.2f} min | Max S11_dB = {max_S11_dB:.2f} dB")

# Customize plot

plt.xlabel('Frequency (GHz)')
plt.ylabel('S21 Magnitude (dB)')
plt.title('S21 vs Frequency at Different Times')
plt.grid(True)
plt.legend(title='Time')
plt.ylim(-65, -50)
plt.figure(figsize=(8,5))
plt.tight_layout()
plt.show()

# Sort by time (optional)
x_minutes = np.array(x_minutes)
y_max_s11_dB = np.array(y_max_s11_dB)
sorted_idx = np.argsort(x_minutes)
x_minutes = x_minutes[sorted_idx]
y_max_s11_dB = y_max_s11_dB[sorted_idx]

# Save to decay.itx
#save_max_s11_to_itx(x_minutes, y_max_s11_dB, "decay.itx")





###############################