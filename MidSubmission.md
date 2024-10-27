# Terra Sense: Mid Submission
Predicting Natural disasters using satellite data

> Team Name: `Paradox Protocol`

### Abstract

Natural disasters pose significant threats to life and property, necessitating advanced predictive measures to mitigate their impacts. Current methodologies often lack the integration of timely satellite data and machine learning techniques, resulting in insufficiently targeted alerts and resource allocation. This research addresses the gap by developing a robust framework to predict natural disasters—specifically hurricanes, earthquakes, and floods—using satellite-derived data and machine learning algorithms. Our primary objective is to identify high-risk areas and provide timely alerts to affected populations.

Employing a combination of satellite data from NASA's Earth Observing System and Sentinel Hub, we implement anomaly detection techniques, such as the Isolation Forest Algorithm, to analyze historical patterns and real-time data. Initial findings demonstrate a notable R² score of 0.791 in predicting maximum temperature, indicating the model's efficacy in leveraging weather forecasting data. Moreover, the ongoing validation of Normalized Difference Water Index (NDWI) analyses underscores our method's potential for flood risk assessment.

The implications of this research are significant: by effectively predicting natural disasters, we can enhance early warning systems and improve emergency response strategies. This framework allows for scalable solutions.

### Machine Learning Algorithms

#### Proof of Work

- Weather Forecasting using Satellite Data and current weather data. Evaluation of the model using R² score. (Completed)
- Anomaly Detection of NDWI(Normalized Difference Water Index) over time using Isolation Forest Algorithm with patch extraction. (Validation in progress)
- **UI**: Based on the provided location, within a 15km radius, identify hot spots and alert either based on proximity or the total % of the area affected.

### Designed for Scale

- *A service to get the patches of cloudy/rainy areas*. This is to reduce the total search space. This can be done using a simple Weather API
- A service to get the NDWI index of the patches (with history to x days, depending on the disaster and other factors)
  - This is to identify the water bodies
  - This can be done using Sentinel Hub API
- As the satellite is not frequently updated (1-2 per day), we can pre-compute the NDWI index and the associated risk factor for the patches
  - This allows us to scale to a larger user base
- All these components can be independently scaled based on the load
