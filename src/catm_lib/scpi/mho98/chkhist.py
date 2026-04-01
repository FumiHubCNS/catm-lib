import h5py
import numpy as np
import matplotlib.pyplot as plt

h5file = "data/pulser_010_1000mV.h5"

with h5py.File(h5file, "r") as f:
    channel_index = f["channel_index"][:]
    voltage_mV = f["voltage_mV"]

    peak_by_channel = {1: [], 2: [], 3: [], 4: []}

    for i in range(len(channel_index)):
        ch = int(channel_index[i])
        v = np.array(voltage_mV[i], dtype=np.float64)

        if v.size == 0:
            continue

        peak = np.max(v)
        peak_by_channel[ch].append(peak)

# ヒストグラム描画
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.ravel()

for ch in [1, 2, 3, 4]:
    ax = axes[ch - 1]
    peaks = np.array(peak_by_channel[ch], dtype=np.float64)

    if peaks.size == 0:
        ax.set_title(f"CH{ch} (no data)")
        continue

    ax.hist(peaks, bins=50)
    ax.set_title(f"CH{ch} peak height histogram")
    ax.set_xlabel("Peak height [mV]")
    ax.set_ylabel("Counts")
    ax.grid(True)

plt.tight_layout()
plt.show()