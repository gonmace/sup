// firebase-service-worker.js
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');

firebase.initializeApp({
    apiKey: "AIzaSyD1JVEEfALYm7AewLXIrWdY1dKognP5Mv8",
    authDomain: "redlinegs-b0c63.firebaseapp.com",
    projectId: "redlinegs-b0c63",
    storageBucket: "redlinegs-b0c63.appspot.com",
    messagingSenderId: "977169881582",
    appId: "1:977169881582:web:10adfc014ae57f87e756ff",
    measurementId: "G-M3E7Y3GH3C"
});

const messaging = firebase.messaging();

// Maneja mensajes en segundo plano
messaging.onBackgroundMessage(function(payload) {
    console.log('[firebase-messaging-sw.js] Recibido mensaje en segundo plano:', payload);

    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: payload.notification.icon,
    };

    if (payload.notification) {
        console.log('La notificación será manejada por el sistema operativo.');
    }
    
    self.registration.showNotification(notificationTitle, notificationOptions);
});
