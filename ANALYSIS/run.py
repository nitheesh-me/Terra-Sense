from pathlib import Path
import h5py
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os

# Function to read subdataset from HDF file
def read_hdf_subdataset(hdf_file, subdataset_name):
    # with h5py.File(hdf_file, 'r') as hdf:
    #     data = hdf[subdataset_name][:]
    # return data
    f = h5py.File(hdf_file, 'r')
    data = f[subdataset_name][:]
    f.close()
    return data

# HDF file path
hdf_file_path = Path('../database/earthdata/MCDWD_L3_NRT.A2024300.h35v13.061.hdf').resolve()

# Define subdatasets to visualize
subdatasets = [
    'Grid_Water_Composite:FloodCS_1Day_250m',
    # 'Grid_Water_Composite:Flood_1Day_250m',
    # 'Grid_Water_Composite:Flood_2Day_250m',
    # 'Grid_Water_Composite:Flood_3Day_250m'
]

# Prepare to save frames for animation
frames = []

for subdataset in subdatasets:
    print(f'Reading subdataset: {subdataset} from {hdf_file_path}')
    data = read_hdf_subdataset(hdf_file_path, subdataset)

    # Normalize the data for visualization
    normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data)) * 255
    normalized_data = normalized_data.astype(np.uint8)

    # Create a figure
    plt.figure(figsize=(10, 10))
    plt.imshow(normalized_data, cmap='Blues', vmin=0, vmax=255)
    plt.colorbar(label='Flood Intensity')
    plt.title(f'Subdataset: {subdataset}')

    # Save the current plot to a frame
    frame_path = f'frame_{subdataset.split(":")[-1]}.png'
    plt.savefig(frame_path)
    plt.close()
    frames.append(frame_path)

# Create an animation
with imageio.get_writer('flood_animation.gif', mode='I', duration=1) as writer:
    for frame in frames:
        image = imageio.imread(frame)
        writer.append_data(image)

# Clean up frame images
for frame in frames:
    os.remove(frame)

print("Animation saved as 'flood_animation.gif'")
