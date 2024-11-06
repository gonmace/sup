// firebase-messaging-sw.js
importScripts('https://www.gstatic.com/firebasejs/9.2.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.2.0/firebase-messaging-compat.js');


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

messaging.onBackgroundMessage(function(payload) {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Personalizar la notificación aquí
  const notificationTitle = 'Background Message Title';
  const notificationOptions = {
    body: payload.notification?.body || 'Background Message body.',
    icon: payload.notification?.image || '/firebase-logo.png'
  };

      // Muestra la notificación solo si no está duplicada
      if (!self.registration.getNotifications) {
        self.registration.showNotification(notificationTitle, notificationOptions);
    }
});

// // Manejo de clic en la notificación
// self.addEventListener('notificationclick', function (event) {
//   event.notification.close();

//   // Redirige a una URL específica cuando se hace clic en la notificación
//   event.waitUntil(
//       clients.matchAll({ type: 'window', includeUncontrolled: true }).then(clientList => {
//           if (clients.openWindow) {
//               return clients.openWindow('google.com'); // Cambia '/' por la URL que desees abrir
//           }
//       })
//   );
// });