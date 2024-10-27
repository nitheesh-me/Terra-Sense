import os
import numpy as np
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from sentinelhub import SHConfig, SentinelHubRequest, DataCollection, bbox_to_dimensions, CRS, BBox, MimeType
from geopy.distance import great_circle
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache
import hashlib
import os

# Load environment variables
env_loc = Path('.') / '.env'
load_dotenv(dotenv_path=env_loc)

# Configure Sentinel Hub
config = SHConfig()
if not config.sh_client_id or not config.sh_client_secret:
    raise Exception("Please provide the Sentinel Hub credentials in the .env file.")

app = FastAPI()

@lru_cache(maxsize=128)
def calculate_bounding_box(lat, lon, radius_km):
    north = great_circle(kilometers=radius_km).destination((lat, lon), 0)  # North
    south = great_circle(kilometers=radius_km).destination((lat, lon), 180)  # South
    east = great_circle(kilometers=radius_km).destination((lat, lon), 90)  # East
    west = great_circle(kilometers=radius_km).destination((lat, lon), 270)  # West
    return [west.longitude, south.latitude, east.longitude, north.latitude]

@lru_cache(maxsize=128)
def get_flood_image(lat, lon, radius_km, time_interval, resolution=60, tot=0.5):
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

    return water_image

def get_range_of_flooding_areas(lat, lon, radius_km, time_interval, skip=1, consider=1, resolution=60, tot=0.5):
    start_date = datetime.strptime(time_interval[0], "%Y-%m-%d")
    end_date = datetime.strptime(time_interval[1], "%Y-%m-%d")
    delta = timedelta(days=skip)
    consider_days = timedelta(days=consider)
    water_images = []
    dates = []

    while start_date <= end_date:
        time_interval = (start_date.strftime("%Y-%m-%d"), (start_date + consider_days).strftime("%Y-%m-%d"))
        water_image = get_flood_image(lat, lon, radius_km, time_interval, resolution, tot)
        water_images.append(water_image)
        dates.append(time_interval[0])
        start_date += delta

    return water_images, dates

def add_text_with_fade(images, texts, fade_steps=10, font_size=20, output_size=None):
    faded_images = []
    font = ImageFont.load_default(font_size)

    for i, img in enumerate(images):
        img = Image.fromarray((img * 255).astype(np.uint8))
        if output_size:
            img = img.resize(output_size)

        draw = ImageDraw.Draw(img)
        text = texts[i] if i < len(texts) else ""
        draw.text((100, 100), text, font=font, fill="#0000FF")

        if i > 0:
            fade_image = faded_images[i - 1].copy()
            fade_factor = 1 - (1 - 0.1) ** (i + 1)
            fade_image = Image.blend(fade_image, img, fade_factor)
            faded_images.append(fade_image)
        else:
            faded_images.append(img)

    return faded_images

def generate_gif(images, filename):
    images[0].save(filename, save_all=True, append_images=images[1:], duration=1000, loop=0)

def get_gif_cache_filename(lat, lon, radius_km, time_interval):
    hash_input = f"{lat}_{lon}_{radius_km}_{time_interval}"
    hash_key = hashlib.md5(hash_input.encode()).hexdigest()
    return f"cache/flooding_{hash_key}.gif"

@app.get("/flood_gif/")
async def create_flood_gif(lat: float, lon: float, radius_km: int=10, start_date:str|None=None, end_date:str|None=None):
    if not start_date or not end_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
    try:
        # Create cache directory if it doesn't exist
        os.makedirs("cache", exist_ok=True)

        gif_path = get_gif_cache_filename(lat, lon, radius_km, (start_date, end_date))

        # Check if the GIF is already cached
        if os.path.exists(gif_path):
            return FileResponse(gif_path, media_type='image/gif')

        time_interval = (start_date, end_date)
        water_images, dates = get_range_of_flooding_areas(
            lat, lon, radius_km, time_interval,
            skip=1, consider=2, resolution=60, tot=0.5
        )

        result_images = add_text_with_fade(water_images, dates, fade_steps=5, font_size=20)

        # Generate and save GIF
        generate_gif(result_images, gif_path)

        return FileResponse(gif_path, media_type='image/gif')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
