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

self.addEventListener("push", function (event) {
    messaging.onBackgroundMessage((payload) => {
        const {
            data: { title, body, actionUrl, icon },
        } = payload;

        const notificationOptions = {
            body,
            icon,
            data: {
                actionUrl,
            },
        };

        const promiseChain = new Promise((resolve) => {
            self.registration
                .showNotification(title, notificationOptions)
                .then(() => resolve());
        });

        event.waitUntil(promiseChain);
    });
});

self.addEventListener("notificationclick", (event) => {
    const { notification } = event;
    const {
      data: { actionUrl },
    } = notification;

    event.notification.close();

    event.waitUntil(
      clients
        .matchAll({ type: "window", includeUncontrolled: true })
        .then((clientsArr) => {
          // If a Window tab matching the targeted URL already exists, focus that;
          const hadWindowToFocus = clientsArr.some((windowClient) => {
            windowClient.url === actionUrl
              ? (windowClient.focus(), true)
              : false;
          });

          // Otherwise, open a new tab to the applicable URL and focus it.
          if (!hadWindowToFocus) {
            return clients.openWindow(actionUrl);
          }
        })
    );
  });