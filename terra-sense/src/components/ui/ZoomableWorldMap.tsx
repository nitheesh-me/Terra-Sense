import React, { useEffect } from 'react';
import L from 'https://cdn.esm.sh/react-leaflet';

const MapComponent = () => {
  useEffect(() => {
    const mapOptions = {
      center: [51.958, 9.141],
      zoom: 10,
    };

    const map = L.map('map', mapOptions);
    const layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
    map.addLayer(layer);

    let marker = null;

    map.on('click', (event) => {
      if (marker !== null) {
        map.removeLayer(marker);
      }

      marker = L.marker([event.latlng.lat, event.latlng.lng]).addTo(map);

      document.getElementById('latitude').value = event.latlng.lat;
      document.getElementById('longitude').value = event.latlng.lng;
    });

    return () => {
      map.remove(); // Clean up the map on component unmount
    };
  }, []);

  return (
    <div className="w-[1200px] mx-auto my-8 grid gap-12 grid-cols-[300px_auto]">
      <form className="form">
        <input
          type="text"
          id="latitude"
          placeholder="latitude"
          className="w-full border-none p-5 text-lg outline-none mb-2 bg-gray-300 rounded-lg transition-all duration-500 focus:bg-gray-400"
        />
        <input
          type="text"
          id="longitude"
          placeholder="longitude"
          className="w-full border-none p-5 text-lg outline-none mb-2 bg-gray-300 rounded-lg transition-all duration-500 focus:bg-gray-400"
        />
        <button
          type="button"
          className="form__btn text-white bg-green-500 py-2 px-4 rounded-lg"
        >
          Submit
        </button>
      </form>
      <div id="map" className="w-full h-[500px] rounded-lg"></div>
    </div>
  );
};

export default MapComponent;
