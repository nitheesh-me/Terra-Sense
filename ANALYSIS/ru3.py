import geemap
import ee

# Initialize the Earth Engine library
ee.Initialize()

class SatelliteImageProcessor:
    def __init__(self, coordinates, start_date, end_date):
        self.coordinates = ee.Geometry.Point(coordinates)
        self.start_date = start_date
        self.end_date = end_date
        self.image_collection = None
        self.image = None

    def fetch_image_collection(self):
        """Fetch the Sentinel-2 image collection for the specified dates."""
        self.image_collection = (
            ee.ImageCollection('COPERNICUS/S2')
            .filterBounds(self.coordinates)
            .filterDate(self.start_date, self.end_date)
        )

    def get_first_image(self):
        """Get the first image from the filtered image collection."""
        self.image = self.image_collection.first()

    def calculate_evi(self):
        """Calculate the Enhanced Vegetation Index (EVI)."""
        evi = self.image.expression(
            'G * ((NIR - Red) / (NIR + C1 * Red - C2 * Blue + L))', {
                'NIR': self.image.select('B8'),
                'Red': self.image.select('B4'),
                'Blue': self.image.select('B2'),
                'G': 2.5,
                'C1': 6,
                'C2': 7.5,
                'L': 1
            })
        return evi

    def calculate_ndmi(self):
        """Calculate the Normalized Difference Moisture Index (NDMI)."""
        ndmi = self.image.normalizedDifference(['B8', 'B11'])
        return ndmi

    def get_true_color(self):
        """Get the True Color image."""
        true_color = self.image.select(['B4', 'B3', 'B2'])
        return true_color

    def visualize(self):
        """Visualize the True Color, EVI, and NDMI images."""
        true_color = self.get_true_color()
        evi = self.calculate_evi()
        ndmi = self.calculate_ndmi()

        # Map setup
        Map = geemap.Map()
        Map.centerObject(self.coordinates, 10)
        Map.addLayer(true_color, {'min': 0, 'max': 3000}, 'True Color')
        Map.addLayer(evi, {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}, 'EVI')
        Map.addLayer(ndmi, {'min': -1, 'max': 1, 'palette': ['red', 'white', 'blue']}, 'NDMI')
        Map.addLayer(self.coordinates, {'color': 'red'}, 'Coordinates')
        Map.add_colorbar(legend_title='EVI', min=0, max=1, palette=['blue', 'white', 'green'])
        Map.add_colorbar(legend_title='NDMI', min=-1, max=1, palette=['red', 'white', 'blue'])

        return Map

# Usage example
if __name__ == "__main__":
    # Replace with your coordinates and date range
    coordinates = [-122.292, 37.901]  # Longitude, Latitude
    start_date = '2023-01-01'
    end_date = '2023-12-31'

    processor = SatelliteImageProcessor(coordinates, start_date, end_date)
    processor.fetch_image_collection()
    processor.get_first_image()

    # Visualize the results
    map_widget = processor.visualize()
    map_widget.show()
