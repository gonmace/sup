// firebase-service-worker.js
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.10.1/firebase-messaging.js');

firebase.initializeApp({

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