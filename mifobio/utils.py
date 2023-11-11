"""Visualisation tools for 3d volumes using matplotlib.

The multislice viewer is copied from:
https://www.datacamp.com/tutorial/matplotlib-3d-volumetric-data.
"""

import matplotlib.pyplot as plt


def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith("keymap."):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)


def multi_slice_viewer(volume, first_index=None, **kwargs):
    remove_keymap_conflicts({"j", "k"})
    fig, ax = plt.subplots()
    ax.volume = volume
    ax.index = first_index if first_index is not None else volume.shape[-1] // 2
    sc = ax.imshow(volume[:, :, ax.index], **kwargs)
    plt.colorbar(sc)
    plt.title(f"{ax.index} / {volume.shape[-1]}")
    fig.canvas.mpl_connect("key_press_event", process_key)


def process_key(event):
    fig = event.canvas.figure
    ax = fig.axes[0]
    if event.key == "j":
        previous_slice(ax)
    elif event.key == "k":
        next_slice(ax)
    fig.canvas.draw()


def previous_slice(ax):
    volume = ax.volume
    ax.index = (ax.index - 1) % volume.shape[-1]  # wrap around using %
    ax.images[0].set_array(volume[:, :, ax.index])
    plt.title(f"{ax.index} / {volume.shape[-1]}")


def next_slice(ax):
    volume = ax.volume
    ax.index = (ax.index + 1) % volume.shape[-1]
    ax.images[0].set_array(volume[:, :, ax.index])
    plt.title(f"{ax.index} / {volume.shape[-1]}")
