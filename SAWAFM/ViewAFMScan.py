# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 14:07:15 2025

@author: Ranjani
"""

import numpy as np
import matplotlib.pyplot as plt
from NSFopen.read import nid_read
import matplotlib.pyplot as plt

def average_amp_vs_x(amp_2nd_lockin, x_range):
    """
    Average the 2nd Lock-In Amplitude over all rows to get amplitude vs x-distance.

    Parameters:
    - amp_2nd_lockin: 2D numpy array (ny rows x nx columns)
    - x_range: float, total physical scan length along x (e.g. in micrometers)

    Returns:
    - x: 1D numpy array of x distances (length nx)
    - amp_avg: 1D numpy array of averaged amplitude over rows (length nx)
    """
    ny, nx = amp_2nd_lockin.shape
    amp_avg = np.mean(amp_2nd_lockin, axis=0)
    x = np.linspace(0, x_range, nx)
    return x, amp_avg

def detrend_lines(image):
    corrected = np.empty_like(image)
    x = np.arange(image.shape[1])
    for i in range(image.shape[0]):
        y = image[i, :]
        p = np.polyfit(x, y, 1)  # linear fit (degree 1)
        trend = np.polyval(p, x)
        corrected[i, :] = y - trend
    return corrected
##################################################



# Read the .nid file
data = nid_read("20250728_00209_longsweepLAOSTO81_D7_f_sweep_-20dBm_2.159153GHz.nid)


# Extract 2nd Lock-In Amplitude (forward)
# amp_2nd_lockin = data.data[('Image', 'Forward', '2nd Lock-In Amplitude')]
amp_2nd_lockin = data.data[('Image', 'Forward', 'Z-Axis')]

amp_2nd_lockin = np.array(amp_2nd_lockin)
amp_2nd_lockin = detrend_lines(amp_2nd_lockin)

# Dimensions
ny, nx = amp_2nd_lockin.shape

# Define real scan ranges (replace these with your actual values)
x_range = 20.0  # micrometers, example
y_range = 20.0

# Create distance arrays
x = np.linspace(0, x_range, nx)
y = np.linspace(0, y_range, ny)

# Plot with physical axes
plt.figure(figsize=(6,5))
plt.imshow(amp_2nd_lockin, extent=[x[0], x[-1], y[-1], y[0]], cmap='inferno', aspect='auto')
plt.colorbar(label='2nd Lock-In Amplitude (units)')
plt.xlabel('X (µm)')
plt.ylabel('Y (µm)')
plt.title('AFM 2nd Lock-In Amplitude (Forward Scan)')

# Save matrix to text file
np.savetxt("IDTtopo.csv", amp_2nd_lockin, delimiter=",", fmt="%.8f")

print("Matrix saved as amp_2nd_lockin_matrix.csv")

# x, amp_avg = average_amp_vs_x(amp_2nd_lockin, x_range)

# plt.plot(x, amp_avg)
# plt.xlabel('X Distance (µm)')
# plt.ylabel('Average 2nd Lock-In Amplitude')
# plt.title('Amplitude vs X Distance')
# plt.show()