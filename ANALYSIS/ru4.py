from sentinelhub import SHConfig
from dotenv import load_dotenv
from pathlib import Path
import os

env_loc = Path('.') / '.env'
load_dotenv(dotenv_path=env_loc)

config = SHConfig()

if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

import datetime
import os

import matplotlib.pyplot as plt
import numpy as np

from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
)

# The following is not a package. It is a file utils.py which should be in the same folder as this notebook.
from utils import plot_image

# betsiboka_coords_wgs84 = (46.16, -16.15, 46.51, -15.58)
AP_coords_wgs84 = (76.75, 12.61, 84.81, 19.92)
# diff / 4
AP_coords_wgs84 = (79.78, 15.27, 80.78, 16.27)
AP_coords_wgs84 = (75.57, 30.38, 79.0, 33.26)
TIME_INTERVAL = ("2024-05-26", "2024-05-28")

resolution = 150

betsiboka_bbox = BBox(bbox=AP_coords_wgs84, crs=CRS.WGS84)
betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

print(f"Image shape at {resolution} m resolution: {betsiboka_size} pixels")

evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""

request_true_color = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=TIME_INTERVAL,
        )
    ],
    responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
    bbox=betsiboka_bbox,
    size=betsiboka_size,
    config=config,
)

true_color_imgs = request_true_color.get_data()

print(f"Returned data is of type = {type(true_color_imgs)} and length {len(true_color_imgs)}.")
print(f"Single element in the list is of type {type(true_color_imgs[-1])} and has shape {true_color_imgs[-1].shape}")

image = true_color_imgs[0]
print(f"Image type: {image.dtype}")

# plot function
# factor 1/255 to scale between 0-1
# factor 3.5 to increase brightness
plot_image(image, factor=3.5 / 255, clip_range=(0, 1), image_type='true_color')

# EVI
evalscript_evi = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B04", "B08", "B02"]
            }],
            output: {
                bands: 1
            }
        };
    }

    function evaluatePixel(sample) {
        let denom = sample.B08 + sample.B04;
        denom = denom == 0 ? 0.0001 : denom; // to prevent division by zero
        let evi = 2.5 * (sample.B08 - sample.B04) / denom;
        return [evi];
    }
"""

request_evi = SentinelHubRequest(
    evalscript=evalscript_evi,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=TIME_INTERVAL,
        )
    ],
    responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
    bbox=betsiboka_bbox,
    size=betsiboka_size,
    config=config,
)

evi_imgs = request_evi.get_data()

print(f"Returned data is of type = {type(evi_imgs)} and length {len(evi_imgs)}.")
print(f"Single element in the list is of type {type(evi_imgs[-1])} and has shape {evi_imgs[-1].shape}")

evi = evi_imgs[0][:, :]
print(f"Image type: {evi.dtype}")

plot_image(evi, factor=3.5, clip_range=(-1, 1), image_type='evi')

# NDMI

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

# Create and execute the request for NDMI
request_ndmi = SentinelHubRequest(
    evalscript=evalscript_ndmi,
    input_data=[SentinelHubRequest.input_data(
        data_collection=DataCollection.SENTINEL2_L1C,
        time_interval=TIME_INTERVAL,
    )],
    responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
    bbox=betsiboka_bbox,
    size=betsiboka_size,
    config=config,
)

ndmi_imgs = request_ndmi.get_data()
print(f"Returned data is of type = {type(ndmi_imgs)} and length {len(ndmi_imgs)}.")
print(f"Single element in the list is of type {type(ndmi_imgs[-1])} and has shape {ndmi_imgs[-1].shape}")

# Display NDMI image
ndmi = ndmi_imgs[0][:, :]
print(f"Image type: {ndmi.dtype}")
plot_image(ndmi, factor=3.5, clip_range=(-1, 1), image_type='ndmi')


# FLood detection
evalscript_flood = """
    //VERSION=3
    function setup() {
        return {
            input: [{ bands: ["B03", "B08", "B02"] }],
            output: { bands: 3 }
        };
    }
    function evaluatePixel(sample) {
        let ndwi = (sample.B03 - sample.B08) / (sample.B03 + sample.B08);
        let ndvi = (sample.B08 - sample.B02) / (sample.B08 + sample.B02);
        let flood = (ndwi > 0.005) && (ndvi > 0.005);
        return [flood, flood, flood];
    }
"""

# Create and execute the request for flood detection
request_flood = SentinelHubRequest(
    evalscript=evalscript_flood,
    input_data=[SentinelHubRequest.input_data(
        data_collection=DataCollection.SENTINEL2_L1C,
        time_interval=TIME_INTERVAL,
    )],
    responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
    bbox=betsiboka_bbox,
    size=betsiboka_size,
    config=config,
)

flood_imgs = request_flood.get_data()
print(f"Returned data is of type = {type(flood_imgs)} and length {len(flood_imgs)}.")
print(f"Single element in the list is of type {type(flood_imgs[-1])} and has shape {flood_imgs[-1].shape}")

# Display flood detection image
flood = flood_imgs[0]
print(f"Image type: {flood.dtype}")
plot_image(flood, factor=3.5, clip_range=(0, 1), image_type='flood_detection')


from flask import Flask, request, jsonify

app = Flask(__name__)

def get_new_flood_hazard_info(lat, lon, radius_km=25, time_interval=TIME_INTERVAL, resolution=60, show=False, tot=0.5):
    """Get new flood hazard information"""
    bbox = BBox(bbox=(lat, lon, lat, lon), crs=CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=resolution)

    evalscript_flood = """
        //VERSION=3
        function setup() {
            return {
                input: [{ bands: ["B03", "B08", "B02"] }],
                output: { bands: 3 }
            };
        }
        function evaluatePixel(sample) {
            let ndwi = (sample.B03 - sample.B08) / (sample.B03 + sample.B08);
            let ndvi = (sample.B08 - sample.B02) / (sample.B08 + sample.B02);
            let flood = (ndwi > 0.005) && (ndvi > 0.005);
            return [flood, flood, flood];
        }
    """

    request_flood = SentinelHubRequest(
        evalscript=evalscript_flood,
        input_data=[SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=time_interval,
        )],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=bbox,
        size=size,
        config=config,
    )

    flood_imgs = request_flood.get_data()

    flood = flood_imgs[0]
    if show:
        plot_image(flood, factor=3.5, clip_range=(0, 1), image_type='flood_detection')

    return flood

@app.route('/alert', methods=['GET'])
def alert():
    """get lat and lon from request, return flood detection image"""
    data = request.get_json()
    lat = data['lat']
    lon = data['lon']
    radius_km = data.get('radius_km', 25)
    time_interval = data.get('time_interval', TIME_INTERVAL)
    resolution = data.get('resolution', 60)
    show = data.get('show', False)
    tot = data.get('tot', 0.5)

    flood = get_new_flood_hazard_info(lat, lon, radius_km, time_interval, resolution, show, tot)

    # if 10% of the image is flooded then return high danger level
    if np.sum(flood) > 0.4 * flood.size:
        danger_level = 'high'
    if np.sum(flood) > 0.1 * flood.size:
        danger_level = 'moderate'
    else:
        danger_level = 'low'
    # return danger level and base64 image
    from PIL import Image
    import io
    import base64

    img = Image.fromarray((flood * 255).astype(np.uint8))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "PNG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())

    return jsonify({
        'danger_level': danger_level,
        'image': img_base64
    })

if __name__ == '__main__':
    app.run(debug=True)
    # testing