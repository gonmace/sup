import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import "leaflet";
import "leaflet.markercluster";
import 'leaflet.markercluster.layersupport';
import "leaflet.control.layers.tree";
import "leaflet.control.layers.tree/L.Control.Layers.Tree.css";

import { yellowIcon, redIcon, greenIcon, blueIcon, grayIcon, nullIcon } from './data/icons.js';
import { osm, osm_dark, ewi } from './data/tiles.js';
import { chartProgreso, diasTranscurridos } from './charts.js';

const carousel = document.getElementById('images-container');
const titulo = document.getElementById('titulo');
const nombre = document.getElementById('nombre');
const cod_id = document.getElementById('cod_id');
const altura = document.getElementById('altura');
const contratista = document.getElementById('contratista');
const comentario = document.getElementById('comentario');
const latitud = document.getElementById('latitud');
const longitud = document.getElementById('longitud');
const googleMaps = document.getElementById('googleMaps');
let sitio_id;

function initCarousel() {
    var carousel = document.querySelector('.carousel');
    var items = carousel.querySelectorAll('.carousel-item');
    var currentIndex = 0;
    // Ocultar todos los elementos excepto el primero
    items.forEach(function (item, index) {
        if (index !== 0) {
            item.classList.add('hidden');
        }
    });

    setInterval(function () {
        items[currentIndex].classList.add('hidden');
        currentIndex = (currentIndex + 1) % items.length;
        items[currentIndex].classList.remove('hidden');
    }, 3000);
}


function updateSite(data) {
    
    var images = data.images;
    var latestDate = data.latest_date;
    var comments = data.comments;
    titulo.innerHTML = data.sitio.sitio;
    nombre.innerHTML = data.sitio.nombre;
    cod_id.innerHTML = `Código Cliente: <span class="font-bold">${data.sitio.cod_id}</span>`;
    altura.innerHTML = `Altura: <span class="font-bold">${data.sitio.altura} metros</span>`;
    contratista.innerHTML = data.sitio.contratista ?
        `Contratista: <span class="font-bold">${data.sitio.contratista}</span>` :
        "";
    
    let lat = data.sitio.lat.toFixed(6);
    let lon = data.sitio.lon.toFixed(6);
    latitud.innerHTML = `Latitud: <span class="font-bold">${lat}</span>`;
    longitud.innerHTML = `Longitud: <span class="font-bold">${lon}</span>`;

    carousel.innerHTML = '';

    googleMaps.classList.remove('hidden');

    let mapUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lon}`;
    
    googleMaps.addEventListener('click', function () {
        // Redirigir al usuario a la URL de Google Maps
        window.open(mapUrl, '_blank'); // Abre Google Maps en una nueva pestaña
    });


    if (images.length === 0 && comments.length === 0) {
        var vacio = document.createElement('div');
        vacio.classList.add('skeleton', 'contenedor', 'w-full', 'h-full', 'flex', 'flex-col', 'justify-center', 'px-2');
        vacio.innerHTML = '<p>No hay imágenes disponibles para este sitio.</p>';
        carousel.appendChild(vacio);
        carousel.classList.toggle('cursor-pointer');
    }


    if (images.length > 0) {
        images.forEach(function (image, index) {
            var carouselItem = document.createElement('div');
            carouselItem.classList.add('carousel-item', 'w-full', 'flex', 'flex-col', 'justify-center');

            var imgElement = document.createElement('img');
            imgElement.src = image.url;
            imgElement.alt = image.description;
            imgElement.classList.add('contenedor', 'mb-2');
            carouselItem.appendChild(imgElement);
            carousel.appendChild(carouselItem);
            carousel.classList.toggle('cursor-pointer');
        });
        initCarousel();
    }

    // Mostrar comentarios
    if (comments.length > 0) {
        var comment = comments[0];
        comentario.innerHTML = '';
        comentario.classList.add('contenedor', 'relative');
        var fecha = document.createElement('p');
        var commentElement = document.createElement('p');
        var autorElement = document.createElement('p');

        fecha.classList.add('absolute', 'top-1');
        fecha.innerHTML = latestDate ? latestDate : "";

        commentElement.classList.add('text-lg');
        commentElement.innerHTML = comment.comentario;

        autorElement.classList.add('absolute', 'italic', 'bottom-1', 'right-2', 'text-gray-600');
        autorElement.innerHTML = `${comment.usuario}`;

        comentario.appendChild(fecha);
        comentario.appendChild(commentElement);
        comentario.appendChild(autorElement);

    } else {
        comentario.classList.remove('contenedor');
        comentario.innerHTML = "";
    }

    chartProgreso(data.progreso);
    diasTranscurridos(data.progreso_gral);
   
}

document.addEventListener("DOMContentLoaded", function () {

    carousel.addEventListener('click', function () {
        const primerHijo = carousel.firstElementChild;
        if (primerHijo && !primerHijo.classList.contains('skeleton')) {
            window.location.href = `imgs/${sitio_id}`;
        }
    });

    // Opacidad para el mapa
    const opacidad = 1;

    let mapZoomLevel = isNaN(localStorage.theZoom) ? 5 : localStorage.theZoom;

    let mapCenter;
    if (!localStorage.lat) {
        let totalLat = sitios.reduce((sum, sitio) => sum + (sitio.lat || 0), 0);
        let totalLon = sitios.reduce((sum, sitio) => sum + (sitio.lon || 0), 0);
        let promedioLat = totalLat / sitios.length;
        let promedioLon = totalLon / sitios.length;
        mapCenter =  [promedioLat, promedioLon]
    } else {
        mapCenter = [localStorage.lat, localStorage.lon];
    }
    

    const map = L.map('map', {
        zoomControl: false,
        center: mapCenter,
        zoom: mapZoomLevel
    });

    let groupASG = L.layerGroup(), /*amarillo*/
        groupEJE = L.layerGroup(), /* verde */
        groupTER = L.layerGroup(), /* azul */
        groupPTG = L.layerGroup(), /* gray */
        groupCAN = L.layerGroup(), /* red */
        groupNULL = L.layerGroup(); /* null */

    let groupsStatus = [groupASG, groupEJE, groupTER, groupPTG, groupCAN, groupNULL];
    let groupsContratista = {};

    contratistas.forEach(contratista => {
        groupsContratista[contratista] = L.layerGroup();
    });

    sitios.forEach(sitio => {
        let marker;        
        switch (sitio.estado) {
            case 'ASG':
                marker = L.marker([sitio.lat, sitio.lon], { icon: yellowIcon }).bindPopup(sitio.sitio);
                marker.addTo(groupASG);
                break;
            case 'EJE':
                marker = L.marker([sitio.lat, sitio.lon], { icon: greenIcon }).bindPopup(sitio.sitio);
                marker.addTo(groupEJE);
                break;
            case 'TER':
                marker = L.marker([sitio.lat, sitio.lon], { icon: blueIcon }).bindPopup(sitio.sitio);
                marker.addTo(groupTER);
                break;
            case 'PTG':
                marker = L.marker([sitio.lat, sitio.lon], { icon: grayIcon }).bindPopup(sitio.sitio);
                marker.addTo(groupPTG);
                break;
            case 'CAN':
                marker = L.marker([sitio.lat, sitio.lon], { icon: redIcon }).bindPopup(sitio.sitio);
                marker.addTo(groupCAN);
                break;
            default:
                marker = L.marker([sitio.lat, sitio.lon], { icon: nullIcon }).bindPopup(sitio.sitio);
                marker.addTo(groupNULL);
                break;
        }
    
        marker.siteId = sitio.id;
        marker.on('click', function () {
            sitio_id = this.siteId;
            // Hacer la llamada AJAX
            fetch(`/get_site_data/?site_id=${sitio_id}`)
                .then(response => response.json())
                .then(data => {
                    updateSite(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
        if (sitio.contratista) {
            marker.addTo(groupsContratista[sitio.contratista.cod]);
        }
    })

    // Activar en el mapa
    map.addLayer(groupEJE);
    // map.addLayer(groupASG);
    // map.addLayer(groupTER);
    // map.addLayer(groupPTG);
    // map.addLayer(groupCAN);
    // map.addLayer(groupNULL);

    var baseTree = {
        label: "<strong>MAPAS BASE</strong>",
        children: [
            { label: "Open Street Map", layer: osm(opacidad).addTo(map) },
            { label: "Esri World Imagery", layer: ewi(opacidad) },
            { label: "Open Street Map Dark", layer: osm_dark(opacidad) },
        ],
    };

    var childrenContratistas = [];
    contratistas.forEach(contratista => {
        childrenContratistas.push({ label: ` ${contratista}`, layer: groupsContratista[contratista].addTo(map) });
    })

    var overlayTree = {
        label: "<strong> SITIOS / PROYECTOS</strong>",
        selectAllCheckbox: 'Un/select all',
        children: [
            {
                label: "<strong> ESTADO</strong>",
                selectAllCheckbox: true,
                children: [
                    {
                        label: `<img src="${static_url}/leaflet/icons/yellow.png" class="inline h-5 mx-1">Asignados`,
                        layer: groupASG
                    },
                    {
                        label: `<img src="${static_url}/leaflet/icons/green.png" class="inline h-5 mx-1">En Ejecución`,
                        layer: groupEJE
                    },
                    {
                        label: `<img src="${static_url}/leaflet/icons/blue.png" class="inline h-5 mx-1">Concluidos`,
                        layer: groupTER
                    },
                    {
                        label: `<img src="${static_url}/leaflet/icons/gray.png" class="inline h-5 mx-1">Postergados`,
                        layer: groupPTG
                    },
                    {
                        label: `<img src="${static_url}/leaflet/icons/red.png" class="inline h-5 mx-1">Cancelados`,
                        layer: groupCAN
                    },
                    { label: '<div class="leaflet-control-layers-separator"></div>' }
                ],
            },
            {
                label: "<strong> CONTRATISTAS</strong>",
                selectAllCheckbox: true,
                children: childrenContratistas
            }
        ],
    };
    // Agregar el control de capas al mapa con el plugin de árbol leaflet.control.layers.tree
    L.control.layers.tree(baseTree, overlayTree, {
        position: "topleft",
        namedToggle: true,
        selectorBack: false,
        closedSymbol: '&#8862; &#x1f5c0;',
        openedSymbol: '&#8863; &#x1f5c1;',
        collapsed: true,
        Layer: { icon: blueIcon },
    }).addTo(map);

    map.on('moveend', () => {
        localStorage.theZoom = map.getZoom();
        var centro = map.getCenter();
        localStorage.lat = centro.lat;
        localStorage.lon = centro.lng;
      });


});
