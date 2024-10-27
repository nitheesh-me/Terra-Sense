import os
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from pathlib import Path
from sentinelhub import SHConfig, SentinelHubRequest, DataCollection, bbox_to_dimensions, CRS, BBox, MimeType
from geopy.distance import great_circle
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# Load environment variables
env_loc = Path('.') / '.env'
load_dotenv(dotenv_path=env_loc)

# Configure Sentinel Hub
config = SHConfig()
if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

def calculate_bounding_box(lat, lon, radius_km):
    north = great_circle(kilometers=radius_km).destination((lat, lon), 0)  # North
    south = great_circle(kilometers=radius_km).destination((lat, lon), 180)  # South
    east = great_circle(kilometers=radius_km).destination((lat, lon), 90)  # East
    west = great_circle(kilometers=radius_km).destination((lat, lon), 270)  # West
    return [west.longitude, south.latitude, east.longitude, north.latitude]

def detect_flooding(lat, lon, radius_km, time_interval, resolution=60, show=False, tot=0.5):
    """ Detect flooding in a given area using Sentinel-2 imagery. """

    bounding_box = calculate_bounding_box(lat, lon, radius_km)
    bbox = BBox(bbox=bounding_box, crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=resolution)

    evalscript_ndmi = """
        //VERSION=3
        function setup() {
            return {
                input: [{ bands: ["B08", "B11"] }],
                output: { bands: 1 }
            };
        }
        function evaluatePixel(sample) {
            let ndmi = (sample.B08 - sample.B11) / (sample.B08 + sample.B11);
            return [ndmi];
        }
    """

    request_ndmi = SentinelHubRequest(
        evalscript=evalscript_ndmi,
        input_data=[SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=time_interval,
        )],
        responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        bbox=bbox,
        size=size,
        config=config,
    )

    response = request_ndmi.get_data()
    ndmi_data = response[0]
    water_mask = ndmi_data > (tot * 255)

    water_image = np.zeros(ndmi_data.shape, dtype=np.float32)
    water_image[water_mask] = 1

    if show:
        plt.imshow(ndmi_data, cmap='gray')
        plt.axis('off')
        plt.title('Flooding Image')
        plt.show()

        plt.imshow(water_image, cmap='Blues')
        plt.axis('off')
        plt.title('Identified Water Areas')
        plt.show()

    return water_image

def get_range_of_flooding_areas(lat, lon, radius_km, time_interval, skip=1, consider=1, resolution=60, show=False, tot=0.5):
    start_date = datetime.strptime(time_interval[0], "%Y-%m-%d")
    end_date = datetime.strptime(time_interval[1], "%Y-%m-%d")
    delta = timedelta(days=skip)
    consider_days = timedelta(days=consider)
    water_images = []
    dates = []

    while start_date <= end_date:
        print(f"Processing for date: {start_date}")
        time_interval = (start_date.strftime("%Y-%m-%d"), (start_date + consider_days).strftime("%Y-%m-%d"))
        water_image = detect_flooding(lat, lon, radius_km, time_interval, resolution, show, tot)
        water_images.append(water_image)
        start_date += delta
        dates.append(time_interval[0])

    return water_images, dates

def add_text_with_fade(images, texts, fade_steps=10, font_size=20, output_size=None):
    faded_images = []
    font = ImageFont.load_default() if not font_size else ImageFont.truetype("arial.ttf", font_size)

    for i, img in enumerate(images):
        img = Image.fromarray((img * 255).astype(np.uint8))
        if output_size:
            img = img.resize(output_size)

        draw = ImageDraw.Draw(img)
        text = texts[i] if i < len(texts) else ""
        draw.text((100, 100), text, font=font, fill=(0, 0, 255))

        if i > 0:
            fade_image = faded_images[i - 1].copy()
            fade_factor = 1 - (1 - 0.1) ** (i + 1)
            fade_image = Image.blend(fade_image, img, fade_factor)
            faded_images.append(fade_image)
        else:
            faded_images.append(img)

    return faded_images

if __name__ == "__main__":
    # Define parameters
    latitude = 17.387140  # Example: Hyderabad
    longitude = 78.491684
    radius_km = 50
    time_interval = ('2023-11-15', '2023-12-21')

    resolution = 60
    water_images, dates = get_range_of_flooding_areas(
        latitude, longitude, radius_km, time_interval,
        skip=1, consider=2, resolution=resolution, show=False, tot=0.5
    )

    result_images = add_text_with_fade(water_images, dates, fade_steps=5, font_size=20)

    result_images[0].save('flooding.gif', save_all=True, append_images=result_images[1:], duration=1000, loop=0)
