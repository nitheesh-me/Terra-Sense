const axios = require('axios');
const querystring = require('querystring');

// Replace with your Sentinel Hub credentials
const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const NASA_API_KEY = process.env.NASA_API_KEY;
if (!CLIENT_ID) throw new Error('CLIENT_ID is required');
// const INSTANCE_ID = 'your_instance_id'; // Your Sentinel Hub instance ID

const getSatelliteImage = async (latitude, longitude) => {
  try {
    // Get OAuth token
    const tokenResponse = await axios.post('https://services.sentinel-hub.com/oauth/token',
        querystring.stringify({grant_type: 'client_credentials'}),
        {
            headers: {
                'Content-Type':'application/x-www-form-urlencoded',
                'Authorization': `Basic ${Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64')}`,
            }
        }
    );

    const accessToken = tokenResponse.data.access_token;

    // Define the request payload
    const requestPayload = {
      "input": {
        "bounds": {
          "bbox": [
            longitude - 0.01, // Adjust the bounding box
            latitude - 0.01,
            longitude + 0.01,
            latitude + 0.01,
          ],
        },
        "data": [{
          "dataSource": "S2_L2A", // Sentinel-2 Level-2A
          "time": "2023-10-01", // Replace with desired date
        }],
      },
      "output": {
        "width": 512,
        "height": 512,
        "responses": [{
          "identifier": "default",
          "format": {
            "type": "image/jpeg",
          },
        }],
      },
    };

    // Fetch the satellite image
    const imageResponse = await axios.post(
      `https://services.sentinel-hub.com/api/v1/process`,
      requestPayload,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    // Save or display the image
    console.log('Image URL:', imageResponse.data.outputs.default.url);
  } catch (error) {
    console.error('Error fetching satellite image:', error);
  }
};

// Example usage
// 17.4065, 78.4772
const latitude = 17.4065; // Example latitude
const longitude = 78.4772; // Example longitude

// getSatelliteImage(latitude, longitude);

const getNasaSatelliteImage = async (latitude, longitude, date) => {
    try {
      // Construct the API URL
      const url = `https://api.nasa.gov/planetary/earth/assets?lon=${longitude}&lat=${latitude}&date=${date}&dim=10.0&api_key=${NASA_API_KEY}`;

      // Fetch the satellite image data
      const response = await axios.get(url);

      // Check if the response contains images
      if (response.data && response.data.url) {
        console.log('Image URL:', response.data.url);
      } else {
        console.log('No image found for the given parameters.');
      }
    } catch (error) {
      console.error('Error fetching satellite image:', error);
    }
  };

  const date = '2023-12-01'; // Replace with desired date
  getNasaSatelliteImage(latitude, longitude, date);