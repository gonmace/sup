import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import "leaflet";
import "leaflet.markercluster";
import 'leaflet.markercluster.layersupport';

import { yellowIcon, redIcon, greenIcon, blueIcon, grayIcon } from './data/icons.js';
import { OpenStreetMap_Mapnik, Esri_WorldImagery, OpenStreetMap_Dark } from './data/tiles.js';

document.addEventListener("DOMContentLoaded", function () {

    // Opacidad para el mapa
    const opacidad = 1;

    let mapZoomLevel = isNaN(localStorage.theZoom) ? 8 : localStorage.theZoom;
    let mapCenter = isNaN(localStorage.lat) ? [-33.68075, -70.93344444] : [localStorage.lat, localStorage.lon];

    var map = L.map('map', {
        center: mapCenter,
        zoom: mapZoomLevel,
        layers: [OpenStreetMap_Mapnik(opacidad)]
    });

});
