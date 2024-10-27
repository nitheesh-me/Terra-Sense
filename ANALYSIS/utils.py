from __future__ import annotations
from typing import Any, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np

def plot_image(
    image: np.ndarray,
    factor: float = 1.0,
    clip_range: Optional[Tuple[float, float]] = None,
    image_type: str = 'true_color',  # Added parameter for image type
    **kwargs: Any
) -> None:
    """Utility function for plotting RGB images with appropriate color palettes.

    Args:
        image (np.ndarray): The image data to be plotted.
        factor (float): Scaling factor for the image.
        clip_range (Optional[Tuple[float, float]]): Range to clip the image values.
        image_type (str): Type of the image ('true_color', 'evi', 'ndmi').
        **kwargs: Additional keyword arguments for plt.imshow.
    """

    # Define colormaps for different image types
    colormaps = {
        'true_color': 'viridis',  # Example for True Color (RGB)
        'evi': 'YlGn',            # Colormap for Enhanced Vegetation Index (EVI)
        'ndmi': 'Blues',          # Colormap for Normalized Difference Moisture Index (NDMI)
        'flood_detection': 'RdYlBu',
    }

    # Get the appropriate colormap
    cmap = colormaps.get(image_type, 'viridis')  # Default to 'viridis' if not recognized

    # Create the plot
    _, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), cmap=cmap, **kwargs)
    else:
        ax.imshow(image * factor, cmap=cmap, **kwargs)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.title(f'Image Type: {image_type.capitalize()}')  # Optional title to indicate image type
    plt.show()
