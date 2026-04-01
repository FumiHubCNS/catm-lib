import h5py
import numpy as np
import matplotlib.pyplot as plt

target_trigger = 1

with h5py.File("data/pulser_010_1000mV.h5", "r") as f:
    trigger_index = f["trigger_index"][:]
    channel_index = f["channel_index"][:]
    time_us = f["time_us"]
    voltage_mV = f["voltage_mV"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    axes = axes.ravel()

    for ch in [1, 2, 3, 4]:
        mask = (trigger_index == target_trigger) & (channel_index == ch)
        indices = np.where(mask)[0]

        ax = axes[ch - 1]
        if len(indices) == 0:
            ax.set_title(f"CH{ch} (no data)")
            continue

        i = indices[0]
        t = np.array(time_us[i])
        v = np.array(voltage_mV[i])

        ax.plot(t, v)
        ax.set_title(f"Trigger {target_trigger}, CH{ch}")
        ax.set_xlabel("Time [us]")
        ax.set_ylabel("Voltage [mV]")
        ax.grid(True)

    plt.tight_layout()
    plt.show()