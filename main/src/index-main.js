import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import "leaflet";
import "leaflet.markercluster";
import 'leaflet.markercluster.layersupport';
import "leaflet.control.layers.tree";
import "leaflet.control.layers.tree/L.Control.Layers.Tree.css";
import "leaflet-control-custom";

import { yellowIcon, redIcon, greenIcon, blueIcon, grayIcon, nullIcon } from './data/icons.js';
import { osm, osm_dark, ewi } from './data/tiles.js';
import { chartProgreso, diasTranscurridos } from './charts.js';

const carousel = document.getElementById('images-container');
const titulo = document.getElementById('titulo');
const nombre = document.getElementById('nombre');
const cod_id = document.getElementById('cod_id');
const altura = document.getElementById('altura');
const operador = document.getElementById('operador');
const contratista = document.getElementById('contratista');
const latitud = document.getElementById('latitud');
const longitud = document.getElementById('longitud');
const googleMaps = document.getElementById('googleMaps');
const avanceID = document.getElementById('avance');
let sitio_id;
let chatNumero;
const lineasChat = 3;
const comentario = document.getElementById('comentario');
const streamer = document.getElementById('streamfield');
const section = streamer.querySelector('section');

const logo = document.getElementById('logo');
logo.src = window.location.origin + logoURL;


function initCarousel() {
    var carousel = document.querySelector('.carousel');
    var items = carousel.querySelectorAll('img');
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
    }, 3500);
}



function updateSite(data) {

    console.log("Recibiendo datos al seleccionar un sitio...");
    sitio_id = data.sitio.id;
    console.log("🚀 ~ updateSite ~ sitio_id:", sitio_id)


    // Datos de imagen y comentarios
    var images = data.images;
    var latestDateImages = data.latest_date_images;
    var comments = data.comments;
    var latestDateComments = data.latest_date_comments;
    titulo.innerHTML = data.sitio.sitio;
    nombre.innerHTML = data.sitio.nombre;

    data.sitio.operador ?
        operador.innerHTML = `Operador: <span class="font-bold">${data.sitio.operador}</span>` :
        operador.innerHTML = "";

    data.sitio.cod_id == '---' ?
        cod_id.innerHTML = `Código Cliente: <span class="font-bold">${data.sitio.cod_id}</span>` :
        cod_id.innerHTML = "";

    data.sitio.altura ?
        altura.innerHTML = `Altura: <span class="font-bold">${data.sitio.altura} metros</span>` :
        altura.innerHTML = "";

    contratista.innerHTML = data.sitio.contratista ?
        `Contratista: <span class="font-bold">${data.sitio.contratista}</span>` :
        "";


    let lat = data.sitio.lat.toFixed(6);
    let lon = data.sitio.lon.toFixed(6);
    latitud.innerHTML = `Latitud: <span class="font-bold">${lat}</span>`;
    longitud.innerHTML = `Longitud: <span class="font-bold">${lon}</span>`;

    googleMaps.classList.remove('hidden');

    let mapUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lon}`;

    googleMaps.addEventListener('click', function () {
        // Redirigir al usuario a la URL de Google Maps
        window.open(mapUrl, '_blank'); // Abre Google Maps en una nueva pestaña
    });

    carousel.innerHTML = '';

    if (images.length === 0) {
        var vacio = document.createElement('div');
        vacio.classList.add('skeleton', 'w-full', 'h-full', 'flex', 'flex-col', 'justify-center', 'px-2');
        vacio.innerHTML = '<p>No hay imágenes disponibles para este sitio.</p>';
        carousel.appendChild(vacio);
        carousel.classList.remove('cursor-pointer');
    }

    function supportsWebP(callback) {
        var testImage = new Image();
        testImage.onload = function () {
            // La imagen se ha cargado, el navegador soporta WebP
            callback(true);
        };
        testImage.onerror = function () {
            // La imagen no se ha cargado, el navegador no soporta WebP
            callback(false);
        };
        // Una imagen WebP muy pequeña en base64
        testImage.src = 'data:image/webp;base64,UklGRi4AAABXRUJQVlA4TCEAAAAvAUAAEB8wAiMw' +
            'AgSSNtse/cXjxyCCmrYNWPwmHRH9jwMA';
    }

    if (images.length > 0) {
         // Crear una lista de promesas para cargar todas las imágenes
         const imagePromises = images.map(async (image) => {
            const imgElement = document.createElement('img');
            imgElement.src = image.url;

            supportsWebP(function (supported) {
                if (supported) {
                    console.log('Este navegador soporta WebP!');
                    imgElement.src = imgElement.src.replace(/\.\w+$/, '.webp');
                } else {
                    console.log('Este navegador NO soporta WebP.');
                    // Aquí puedes colocar la lógica para cargar imágenes en otro formato
                }
            });


            imgElement.alt = image.description;
            imgElement.classList.add('object-cover');
            carousel.appendChild(imgElement);

            // Crear contenedor para el texto de fecha
            const dateContainer = document.createElement('div');
            dateContainer.classList.add(
                'absolute',
                'bottom-0',
                'right-0',
                'p-2',
                'sombra',
                'text-white',
                'rounded-tl-lg',
                'rounded-br-lg'
            );

            dateContainer.textContent = latestDateImages;
            carousel.appendChild(dateContainer);
            carousel.classList.add('cursor-pointer');
        });

        // Esperar a que todas las promesas de las imágenes se resuelvan
        Promise.all(imagePromises).then(() => {
            initCarousel();
        });

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
        fecha.innerHTML = latestDateComments ? latestDateComments : "";

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

    if (data.progreso) {
        avanceID.style.height = '16rem';
    } else {
        avanceID.style.height = '0';
    }

    // if (data.progreso_gral) {
    //     avanceID.style.height = '0rem';
    // } else {
    //     avanceID.style.height = '0';
    // }
    chartProgreso(data.progreso);
    diasTranscurridos(data.progreso_gral);
}


function createMessageHTML(
    usuario_id,
    usuario_nombre,
    datetime,
    mensaje
) {
    const nombres = usuario_nombre.split(' ');
    const iniciales = nombres.map(nombre => nombre.charAt(0).toUpperCase()).join('');
    const inicialNombre = nombres[0].charAt(0).toUpperCase() + '.';
    const inicialNombreYApellido = nombres.length > 1 ? inicialNombre + ' ' + nombres[1] : inicialNombre;

    const backgroundColorClass = usuario_id === usuarioID ? 'bg-red-500' : 'bg-yellow-500';
    const chatClass = usuario_id === usuarioID ? 'chat-me' : 'chat-them';
    return `
        <div class="chat-image">
            <div class="${backgroundColorClass} globo-chat">
                <p class="text-white text-sm">${iniciales}</p>
            </div>
        </div>
        <div class="chat-header">
            ${inicialNombreYApellido}
            <time class="text-xs opacity-50">${datetime}</time>
        </div>
        <div class="${chatClass}">${mensaje}</div>
    `;
}

function fetchChats(sitio_id, usuarioID, limite = lineasChat, divID = 'mensajes') {
    fetch(`/get_chats/${sitio_id}/${limite}`)
        .then(response => response.text())
        .then(resp => {
            const data = JSON.parse(resp);
            // Verifica si data es una lista vacía
            if (data.length === 0) {
                console.log("Chat vacio...");
                if (!section.classList.contains('hidden')) {
                    section.classList.add('hidden');
                }
                return;
            }
            section.classList.remove('hidden');
            chatNumero = data[0].chat_id;
            console.log("Recibiendo datos del chat....");

            const messagesContainer = document.getElementById(divID);
            messagesContainer.innerHTML = '';  // Limpia el contenedor antes de agregar nuevos mensajes
            data.reverse().forEach(item => {
                const messageElement = document.createElement('div');
                messageElement.classList.add('chat');
                if (item.usuario_id === usuarioID) {
                    messageElement.classList.add('chat-end', 'relative');
                } else {
                    messageElement.classList.add('chat-start');
                }

                messageElement.innerHTML = createMessageHTML(
                    item.usuario_id,
                    item.usuario_nombre,
                    item.datetime,
                    item.mensaje
                );
                // Añadir el atributo de datos que contiene el ID del item
                messageElement.dataset.itemId = item.id;

                messagesContainer.appendChild(messageElement);


            });
            setTimeout(() => {
                messagesContainer.parentElement.scrollTo({
                    top: messagesContainer.parentElement.scrollHeight,
                    behavior: 'smooth' // Añade un desplazamiento suave
                });
            }, 500); // Ajusta este tiempo si es necesario
            // Si es 0, abre el modelo de chat
            if (limite !== 0) {
                if (messagesContainer.lastChild.classList.contains('chat-end')) {
                    messagesContainer.lastChild.classList.add('mr-10');
                    // Crear el botón
                    const botonBorrarChat = document.createElement('button');
                    botonBorrarChat.innerHTML = `<svg viewBox="0 0 48 48">
	                                        <path fill="none" stroke="black" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" d="M18.424 10.538A2 2 0 0 1 19.788 10H42a2 2 0 0 1 2 2v24a2 2 0 0 1-2 2H19.788a2 2 0 0 1-1.364-.538L4 24zM36 19L26 29m0-10l10 10" />
                                        </svg>`;
                    botonBorrarChat.classList.add('absolute', '-right-12', 'bottom-0', 'w-10', 'btn', 'border-0', '!p-1', 'bg-base-100');
                    messagesContainer.lastChild.appendChild(botonBorrarChat);

                    // Agregar el evento de clic al botón
                    botonBorrarChat.addEventListener('click', () => {
                        const itemId = messagesContainer.lastChild.dataset.itemId;
                        console.log("🚀 itemId:", itemId)
                        console.log("🚀 ChatId:", chatNumero)
                        fetch(`/delete_chat/${chatNumero}/${itemId}`, {
                            method: 'GET'
                        })
                            .then(response => response.json())
                            .then(result => {
                                if (result.errors) {
                                    // Aquí debes manejar y mostrar los errores
                                    console.error('Errores:', result.errors);
                                } else {
                                    console.log('Mensaje: ', result.message);
                                    // TODO Revisar se actualiza el contenedor con websocket

                                }
                            })
                    });


                }
            }
        })
        .catch(error => () => {
            console.error("Error loading chats:", error)
        });

}



function fetchData(sitio_id) {
    // primero borrar los chart de echarts para que se pueda actualizar cuando se cambioe de sitio
    let chartBarras = document.getElementById('barras-Chart');
    chartBarras.innerHTML = '';
    chartBarras.removeAttribute('_echarts_instance_');
    chartBarras.removeAttribute('style');

    let chartGauge = document.getElementById('avance-Chart');
    chartGauge.innerHTML = '';
    chartGauge.removeAttribute('_echarts_instance_');
    chartGauge.removeAttribute('style');

    const form = document.getElementById('message-form');
    // const messagesContainer = document.getElementById('mensajes');

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(form);
            const url = form.action;

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(result => {
                    if (result.errors) {
                        console.error('Errores:', result.errors);
                    } else {
                        console.log('Mensaje enviado con éxito:', result.message);
                        form.reset();
                    }
                })
                .catch(error => {
                    console.error('Error al enviar el formulario:', error);
                });
        });
    } else {
        console.error('El formulario no se encontró en el DOM.');
    }






    var expandButton = document.getElementById('expand-chat');
    // Agrega el listener de eventos
    expandButton.addEventListener('click', async () => {
        await fetchChats(sitio_id, usuarioID, 0, 'chat-all');
        document.getElementById('modal_chat').checked = true;
        document.getElementById('id_sitio_id').value = sitio_id;


    });

    // Agregar sitio id al formulario para el CHAT
    document.getElementById('id_sitio_id').value = sitio_id;

    fetch(`/get_site_data/?site_id=${sitio_id}`)
        .then(response => response.json())
        .then(data => {
            updateSite(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });

    fetch(`/componentes/${sitio_id}`)
        .then(response => response.json())
        .then(data => {
            const div = document.createElement('div'); // Crear un nuevo div para recibir el contenido
            div.innerHTML = data.html;                // Insertar el HTML recibido

            // Mantener el primer hijo y reemplazar el resto
            while (streamer.children.length > 1) {
                streamer.removeChild(streamer.lastChild); // Elimina todos los hijos excepto el primero
            }

            // Añadir el nuevo contenido
            while (div.firstChild) {
                streamer.appendChild(div.firstChild); // Añade los nuevos nodos uno por uno
            }
        })

        .catch(() => {
            // Si hay un error, asegúrate de dejar el primer hijo y quitar el resto
            while (streamfield.children.length > 1) {
                streamfield.removeChild(streamfield.lastChild);
            }

        });

    fetchChats(sitio_id, usuarioID, lineasChat);

}


document.addEventListener("DOMContentLoaded", function () {
    // Inicializar WebSocket
    // WEBSOCKET
    const hostname = window.location.hostname;
    const wsProtocol = (window.location.protocol === 'https:') ? 'wss' : 'ws';
    const wsPort = (hostname === 'localhost') ? ':8000' : ''; // No usar puerto en producción
    const wsPath = '/ws/mensajes/';
    const wsUrl = `${wsProtocol}://${hostname}${wsPort}${wsPath}`;

    const ws = new WebSocket(wsUrl);

    ws.onopen = function () {
        console.log('WebSocket connection established.');
    };

    ws.onerror = function (error) {
        console.error('WebSocket error:', error);
    };

    ws.onmessage = function (e) {
        console.log('Received:', e.data);
        const data = JSON.parse(e.data);
        // Activar función dependiendo del mensaje
        if (data.message) {
            handleMessage(data.message);
        }
    };

    function handleMessage(message) {
        // Aquí puedes añadir cualquier lógica que desees ejecutar en el cliente
        console.log('Handling message:', message);
        if (message.chat == chatNumero) {
            console.log("Atualizando Chat...");
            fetchChats(sitio_id, usuarioID, lineasChat);
        }


    }














    // Mostrar lo sitios en una tabla
    const tbody = document.getElementById('sitios-table-body');

    sitios.forEach((sitio) => {
        const row = tbody.insertRow();
        row.style.cursor = 'pointer';
        row.insertCell().textContent = sitio.sitio;
        row.insertCell().textContent = sitio.cod_id;
        row.insertCell().textContent = sitio.nombre;
        row.insertCell().textContent = sitio.estado;
        row.insertCell().textContent = sitio.contratista.cod
        row.insertCell().textContent = sitio.ito


        // Agregar evento de clic a la fila para ejecutar las funciones
        row.addEventListener('click', function () {
            document.getElementById('modal_sitios').checked = false;

            fetchData(sitio.id);

            var newLatLng = new L.LatLng(sitio.lat, sitio.lon);
            var zoomLevel = 11;

            map.flyTo(newLatLng, zoomLevel, {
                animate: true,
                duration: 3
            });


        });

    });


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
        mapCenter = [promedioLat, promedioLon]
    } else {
        mapCenter = [localStorage.lat, localStorage.lon];
    }

    const map = L.map('map', {
        zoomControl: false,
        center: mapCenter,
        zoom: mapZoomLevel
    });

    L.control.custom({
        position: 'bottomright',
        content: `<div class="h-10 w-10">
         <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
	                    <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-miterlimit="10" stroke-width="1.5" d="M3 15h18M3 9h18M9 21V3m6 18V3M5.4 3h13.2A2.4 2.4 0 0 1 21 5.4v13.2a2.4 2.4 0 0 1-2.4 2.4H5.4A2.4 2.4 0 0 1 3 18.6V5.4A2.4 2.4 0 0 1 5.4 3" />
                    </svg>
                    </div>`,
        classes: 'w-15 h-15',
        style:
        {
            margin: '10px',
            padding: '0px 0 0 0',
            cursor: 'pointer',
        },
        events:
        {
            click: function (data) {
                document.getElementById('modal_sitios').checked = true;
            },
        }
    })
        .addTo(map);

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
            // Recuperar imagenes y avance
            fetchData(sitio_id);
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

    // fetchData(115)
});
