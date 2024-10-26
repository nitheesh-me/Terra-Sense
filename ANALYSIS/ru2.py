import requests
import base64
from PIL import Image
import io
import datetime
import os
# env
from dotenv import load_dotenv
from pathlib import Path
import matplotlib.pyplot as plt


env_loc = Path('.') / '.env'
load_dotenv(dotenv_path=env_loc)

# Constants for Sentinel Hub API
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

# Function to obtain access token
def get_access_token(client_id, client_secret):
    """Fetch access token from Sentinel Hub API."""
    auth_string = f"{client_id}:{client_secret}"
    base64_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64_auth}"
    }

    payload = {"grant_type": "client_credentials"}

    response = requests.post("https://services.sentinel-hub.com/oauth/token", data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to retrieve access token: {response.json()}")

# Function to fetch image from Sentinel Hub API
def fetch_image(evalscript, bbox, date_from, date_to, access_token):
    """Fetch image from Sentinel Hub based on evalscript and date range."""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
            },
            "data": [{
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": f"{date_from}T00:00:00Z",
                        "to": f"{date_to}T23:59:59Z"
                    }
                }
            }]
        },
        "output": {"width": 512, "height": 512},
        "evalscript": evalscript
    }

    from pprint import pprint
    pprint(payload)
    response = requests.post("https://services.sentinel-hub.com/api/v1/process", headers=headers, json=payload)

    if response.status_code == 200:
        breakpoint()
        return Image.open(io.BytesIO(response.content))
    else:
        raise Exception(f"Error fetching image: {response.json()}")

# Main function to get images based on location, date, and time
def get_live_images_based_on_location(lat, lon, date, time):
    """
    Get True color, EVI, and NDMI images from Sentinel Hub API based on location, date, and time.
    """
    # Obtain access token
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)

    # Format date and time
    date_from = date
    date_to = date
    padding = 0.1       # Padding for bbox
    bbox = [lon - padding, lat - padding, lon + padding, lat + padding]  # Adjust bbox size if needed

    # Define evalscripts for each image type
    true_color_evalscript = """
        // VERSION=3
        function setup() {
            return {
                input: ["B02", "B03", "B04"],
                output: { bands: 3 }
            };
        }

        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """

    evi_evalscript = """
        // VERSION=3
        function setup() {
            return {
                input: ["B04", "B08", "B02"],
                output: { bands: 1 }
            };
        }

        function evaluatePixel(sample) {
            let EVI = 2.5 * (sample.B08 - sample.B04) / (sample.B08 + 6 * sample.B04 - 7.5 * sample.B02 + 1);
            return [EVI];
        }
    """

    ndmi_evalscript = """
        // VERSION=3
        function setup() {
            return {
                input: ["B08", "B11"],
                output: { bands: 1 }
            };
        }

        function evaluatePixel(sample) {
            let NDMI = (sample.B08 - sample.B11) / (sample.B08 + sample.B11);
            return [NDMI];
        }
    """

    # Fetch images
    true_color_image = fetch_image(true_color_evalscript, bbox, date_from, date_to, access_token)
    evi_image = fetch_image(evi_evalscript, bbox, date_from, date_to, access_token)
    ndmi_image = fetch_image(ndmi_evalscript, bbox, date_from, date_to, access_token)

    # Display images
    # true_color_image.show(title="True Color")
    # evi_image.show(title="EVI")
    # ndmi_image.show(title="NDMI")

    # Return images
    return {
        "True Color": true_color_image,
        "EVI": evi_image,
        "NDMI": ndmi_image
    }

# Example usage
values = get_live_images_based_on_location(17.4065, 78.4772, '2024-05-01', '12:00:00')

# show the images
f = plt.figure(figsize = (10, 10))
plt.subplot(1, 3, 1)
plt.imshow(values["True Color"])
plt.title('True Color')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(values["EVI"])
plt.title('EVI')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(values["NDMI"])
plt.title('NDMI')
plt.axis('off')

plt.show()
