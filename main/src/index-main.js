import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import "leaflet";
import "leaflet.markercluster";
import 'leaflet.markercluster.layersupport';

import { yellowIcon, redIcon, greenIcon, blueIcon, grayIcon, nullIcon } from './data/icons.js';
import { OpenStreetMap_Mapnik, Esri_WorldImagery, OpenStreetMap_Dark } from './data/tiles.js';


function updateImages(data) {
    
    var images = data.images;
    var latestDate = data.latest_date;
    var comments = data.comments;
    let carousel = document.getElementById('images-container');
    const sitio = document.getElementById('sitio');
    const nombre = document.getElementById('nombre');
    const cod_id = document.getElementById('cod_id');
    const altura = document.getElementById('altura');
    const contratista = document.getElementById('contratista');
    const comentario = document.getElementById('comentario');
    const autor = document.getElementById('autor');
    const dateElement = document.getElementById('fecha');
    sitio.innerHTML = data.sitio.sitio;
    nombre.innerHTML = data.sitio.nombre;
    cod_id.innerHTML = `Codigo Cliente: <span class="font-bold">${data.sitio.cod_id}</span>`;
    altura.innerHTML = `Altura: <span class="font-bold">${data.sitio.altura} metros</span>`;
    dateElement.innerHTML = latestDate ? latestDate : "";
    contratista.innerHTML = data.sitio.contratista ?
    `Contratista: <span class="font-bold">${data.sitio.contratista}</span>` :
    "";

    carousel.innerHTML = '';

    if (images.length === 0 && comments.length === 0) {
        var vacio = document.createElement('div');
        vacio.classList.add('skeleton', 'contenedor', 'w-full', 'h-full', 'flex', 'flex-col', 'justify-center');
        vacio.innerHTML = '<p>No hay imágenes disponibles para este sitio.</p>';
        carousel.appendChild(vacio);
    }


    if (images.length > 0) {    
        images.forEach(function(image, index) {
            var carouselItem = document.createElement('div');
            carouselItem.classList.add('carousel-item', 'w-full', 'flex', 'flex-col', 'justify-center');
    
            var imgElement = document.createElement('img');
            imgElement.src = image.url;
            imgElement.alt = image.description;
            imgElement.classList.add('contenedor', 'mb-2');
            carouselItem.appendChild(imgElement);
            carousel.appendChild(carouselItem);
        });
    
        initCarousel();
    }

    // Mostrar comentarios
    if (comments.length > 0) {
        comentario.innerHTML = '';
        comentario.classList.add('contenedor');
        var comment = comments[0];
        var commentElement = document.createElement('p');
        var autorElement = document.createElement('p');

        commentElement.classList.add('mb-4', 'font-semibold');
        commentElement.innerHTML = comment.comentario;

        autorElement.classList.add('italic', 'text-right', 'text-sm', 'text-gray-600');
        autorElement.innerHTML = `${comment.usuario}`;
        comentario.appendChild(commentElement);
        comentario.appendChild(autorElement);

    } else {
        comentario.classList.remove('contenedor');
        comentario.innerHTML = "";
    }
}


function initCarousel() {
    var carousel = document.querySelector('.carousel');
    var items = carousel.querySelectorAll('.carousel-item');
    var currentIndex = 0;

    // Ocultar todos los elementos excepto el primero
    items.forEach(function(item, index) {
        if (index !== 0) {
            item.classList.add('hidden');
        }
    });

    setInterval(function() {
        items[currentIndex].classList.add('hidden');
        currentIndex = (currentIndex + 1) % items.length;
        items[currentIndex].classList.remove('hidden');
    }, 3000);
}



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

    let groupASG = L.layerGroup(), /*amarillo*/
    groupEJE = L.layerGroup(), /* verde */
    groupTER = L.layerGroup(), /* azul */
    groupPTG = L.layerGroup(), /* gray */
    groupCAN = L.layerGroup(), /* red */
    groupNULL = L.layerGroup(); /* null */

    sitios.forEach(sitio => {
        let marker;
        if (sitio.avance && sitio.avance.estado) {
            switch (sitio.avance.estado) {
                case 'ASG':
                    marker = L.marker([sitio.lat, sitio.lon], { icon: yellowIcon }).bindPopup(sitio.popup);
                    marker.addTo(groupASG);
                    break;
                case 'EJE':
                    marker = L.marker([sitio.lat, sitio.lon], { icon: greenIcon }).bindPopup(sitio.popup);
                    marker.addTo(groupASG);
                    break;
                case 'TER':
                    marker = L.marker([sitio.lat, sitio.lon], { icon: blueIcon }).bindPopup(sitio.popup);
                    marker.addTo(groupTER);
                    break;
                case 'PTG':
                    marker = L.marker([sitio.lat, sitio.lon], { icon: grayIcon }).bindPopup(sitio.popup);
                    marker.addTo(groupPTG);
                    break;
                case 'CAN':
                    marker = L.marker([sitio.lat, sitio.lon], { icon: redIcon }).bindPopup(sitio.popup);
                    marker.addTo(groupCAN);
                    break;
                default:
                    marker = L.marker([sitio.lat, sitio.lon], { icon: nullIcon }).bindPopup(sitio.popup);
                    marker.addTo(groupNULL);
                    break;
            }
        } else {
            marker = L.marker([sitio.lat, sitio.lon], { icon: nullIcon }).bindPopup(sitio.popup);
            marker.addTo(groupNULL);
        }        
        marker.siteId = sitio.id;
        marker.on('click', function() {
            var siteId = this.siteId;
            // Hacer la llamada AJAX
            fetch(`/get_site_images/?site_id=${siteId}`)
                .then(response => response.json())
                .then(data => {
                    updateImages(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
                

        
    })

    map.addLayer(groupEJE);
    map.addLayer(groupASG);
    map.addLayer(groupTER);
    map.addLayer(groupPTG);
    map.addLayer(groupCAN);
    map.addLayer(groupNULL);

});
