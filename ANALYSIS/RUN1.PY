import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load the HDF4 file
hdf_file_path = "../database/earthdata/MCDWD_L3_NRT.A2024300.h35v13.061.hdf"
hdf = SD(hdf_file_path, SDC.READ)

# Extract the relevant datasets
flood_1day = hdf.select('Flood_1Day_250m')[:]
flood_2day = hdf.select('Flood_2Day_250m')[:]

total_counts_1day = hdf.select('TotalCounts_1Day_250m')[:]

# Ensure the images are the correct shape (512x512)
flood_1day = flood_1day.reshape(512, 512)
flood_2day = flood_2day.reshape(512, 512)
total_counts_1day = total_counts_1day.reshape(512, 512)

# Create a mask for valid data (not NaN)
valid_mask = ~np.isnan(flood_1day) & ~np.isnan(flood_2day) & ~np.isnan(total_counts_1day)

# Apply the mask to calculate the change in flood
change_in_flood = np.where(valid_mask, flood_2day - flood_1day, np.nan)

# Reshape the datasets to 1D for analysis using the mask
flood_1day_flat = flood_1day[valid_mask].flatten()
flood_2day_flat = flood_2day[valid_mask].flatten()
total_counts_1day_flat = total_counts_1day[valid_mask].flatten()
change_in_flood_flat = change_in_flood[valid_mask].flatten()

# Create a DataFrame
data = pd.DataFrame({
    'Flood_1Day': flood_1day_flat,
    'Flood_2Day': flood_2day_flat,
    'TotalCounts_1Day': total_counts_1day_flat,
    'ChangeInFlood': change_in_flood_flat
})

# Define features and target for modeling
X = data[['Flood_1Day', 'Flood_2Day', 'TotalCounts_1Day', 'ChangeInFlood']]
y = (data['Flood_1Day'] > 0).astype(int)  # Target: 1 if flooding, 0 otherwise

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Visualization of Change in Flood
plt.figure(figsize=(10, 6))
plt.imshow(change_in_flood, cmap='Blues', interpolation='nearest')
plt.colorbar(label='Change in Flood (2-Day - 1-Day)')
plt.title('Change in Flood Data')
plt.xlabel('Pixel X Coordinate')
plt.ylabel('Pixel Y Coordinate')
plt.show()

# Optional: Visualization of the original flood data
plt.figure(figsize=(10, 6))
plt.imshow(flood_1day, cmap='Blues', interpolation='nearest')
plt.colorbar(label='Flood Data (1-Day)')
plt.title('1-Day Flood Data')
plt.xlabel('Pixel X Coordinate')
plt.ylabel('Pixel Y Coordinate')
plt.show()
