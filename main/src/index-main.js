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


import * as echarts from 'echarts/core';
import {
    DatasetComponent,
    GridComponent,
    VisualMapComponent
} from 'echarts/components';
import { BarChart } from 'echarts/charts';
import { CanvasRenderer } from 'echarts/renderers';


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
    latitud.innerHTML = `Latitud: <span class="font-bold">${data.sitio.lat}</span>`;
    longitud.innerHTML = `Longitud: <span class="font-bold">${data.sitio.lon}</span>`;

    carousel.innerHTML = '';

    googleMaps.classList.remove('hidden');

    googleMaps.addEventListener('click', function () {
        const lat = data.sitio.lat;
        const lon = data.sitio.lon;
        const mapUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lon}`;
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

        autorElement.classList.add('italic', 'text-right', 'text-sm', 'text-gray-600');
        autorElement.innerHTML = `${comment.usuario}`;

        comentario.appendChild(fecha);
        comentario.appendChild(commentElement);
        comentario.appendChild(autorElement);

    } else {
        comentario.classList.remove('contenedor');
        comentario.innerHTML = "";
    }
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

    let mapZoomLevel = isNaN(localStorage.theZoom) ? 8 : localStorage.theZoom;
    let mapCenter = isNaN(localStorage.lat) ? [-33.68075, -70.93344444] : [localStorage.lat, localStorage.lon];

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
        if (sitio.avance && sitio.avance.estado) {
            switch (sitio.avance.estado) {
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
        } else {
            marker = L.marker([sitio.lat, sitio.lon], { icon: nullIcon }).bindPopup(sitio.sitio);
            marker.addTo(groupNULL);
        }
        marker.siteId = sitio.id;
        marker.on('click', function () {
            sitio_id = this.siteId;
            // Hacer la llamada AJAX
            fetch(`/get_site_images/?site_id=${sitio_id}`)
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
                    {
                        label: `<img src="${static_url}/leaflet/icons/null.png" class="inline h-5 mx-1">Sin establecer`,
                        layer: groupNULL
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
        collapsed: false,
    }).addTo(map);

    // ECHARTS

    echarts.use([
        DatasetComponent,
        GridComponent,
        VisualMapComponent,
        BarChart,
        CanvasRenderer
    ]);

    var chartDom = document.getElementById('charts');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        dataset: {
          source: [
            ['score', 'amount', 'product'],
            [89.3, 58212, 'Matcha Latte'],
            [57.1, 78254, 'Milk Tea'],
            [74.4, 41032, 'Cheese Cocoa'],
            [50.1, 12755, 'Cheese Brownie'],
            [89.7, 20145, 'Matcha Cocoa'],
            [68.1, 79146, 'Tea'],
            [19.6, 91852, 'Orange Juice'],
            [10.6, 101852, 'Lemon Juice'],
            [32.7, 20112, 'Walnut Brownie']
          ]
        },
        grid: { containLabel: true },
        xAxis: { name: 'amount' },
        yAxis: { type: 'category' },
        visualMap: {
          orient: 'horizontal',
          left: 'center',
          min: 10,
          max: 100,
          text: ['High Score', 'Low Score'],
          // Map the score column to color
          dimension: 0,
          inRange: {
            color: ['#65B581', '#FFCE34', '#FD665F']
          }
        },
        series: [
          {
            type: 'bar',
            encode: {
              // Map the "amount" column to X axis.
              x: 'amount',
              // Map the "product" column to Y axis
              y: 'product'
            }
          }
        ]
      };
      
      option && myChart.setOption(option);



});
