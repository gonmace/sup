// Initialize Firebase
if (!firebase.apps.length) {
    firebase.initializeApp({
        apiKey: import.meta.env.FIREBASE_API_KEY,
        authDomain: import.meta.env.FIREBASE_AUTH_DOMAIN,
        projectId: import.meta.env.FIREBASE_PROJECT_ID,
        storageBucket: import.meta.env.FIREBASE_STORAGE_BUCKET,
        messagingSenderId: import.meta.env.FIREBASE_MESSAGING_SENDER_ID,
        appId: import.meta.env.FIREBASE_APP_ID,
        measurementId: import.meta.env.FIREBASE_MEASUREMENT_ID
    });
}

const messaging = firebase.messaging();

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('firebase-messaging-sw.js')
        .then((registration) => {
            console.log('Service Worker registered with scope:', registration.scope);

            messaging.useServiceWorker(registration);

            messaging.requestPermission()
                .then(() => {
                    console.log('Notification permission granted.');
                    return messaging.getToken({ vapidKey: 'BINXFXJWk3U5VbOvxRrqmv5HFVLDexKosPJ-Ze_-qrCFeyoxfVYXsFxIfONDG0H7dFx7u89BhJnARefTBn91eiw' });
                })
                .then((token) => {
                    if (token) {
                        console.log('FCM Token:', token);
                        saveFcmToken(token);
                    } else {
                        console.log('No registration token available. Request permission to generate one.');
                    }
                })
                .catch((err) => {
                    console.log('Unable to get permission to notify.', err);
                });

        }).catch((err) => {
            console.log('Service Worker registration failed:', err);
        });
}

const showNotification = (payload) => {
    const {
      // It's better to send notifications as Data Message to handle it by your own SDK
      // See https://firebase.google.com/docs/cloud-messaging/concept-options#notifications_and_data_messages
      data: { title, body, actionUrl, icon },
    } = payload;

    // See https://developer.mozilla.org/docs/Web/API/Notification
    const notificationOptions = {
      body,
      icon,
    };
    
    const notification = new window.Notification(title, notificationOptions);

    notification.onclick = (event) => {
      event.preventDefault(); // prevent the browser from focusing the Notification's tab
      window.open(actionUrl, "_blank").focus();
    };
  };

messaging.onMessage((payload) => {
    console.log("🚀 ~ messaging.onMessage ~ payload:", payload)

    showNotification(payload);
	
    	// console.log("==============");
    	// console.log(payload);
    	// console.log("==============");
    	
    	// let title = payload.notification.title;
    	// let options = {
    	//     body: payload.notification.body,
    	//     icon: payload.notification.icon,
    	// };
	
    	// console.log('Notification received. Title:', title, 'Body:', payload.notification.body, 'Icon:', payload.notification.icon);
	
	
});


async function getDeviceOS() {
    const userAgent = navigator.userAgent;

    if (/windows phone/i.test(userAgent)) {
        return "Windows Phone";
    }
    if (/android/i.test(userAgent)) {
        return "Android";
    }
    if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
        return "iOS";
    }
    if (/Win/i.test(userAgent)) {
        return "Windows";
    }
    if (/Mac/i.test(userAgent)) {
        return "MacOS";
    }
    if (/Linux/i.test(userAgent)) {
        return "Linux";
    }
    return "Desconocido";
}


// Function to save FCM token (ensure this endpoint is correctly set up)
async function saveFcmToken(token) {
    const deviceOS = await getDeviceOS();
    try {
        const response = await fetch('/save_token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(
                {
                    fcm_token: token,
                    device_os: deviceOS
                }
            )
        })

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error al guardar el token:', errorData.message);
        } else {
            const data = await response.json();
            console.log('Respuesta del servidor:', data.message);
        }
    } catch (error) {
        console.error('No se pudo guardar el token:', error);
    }

}

// Example function to get CSRF token from cookies
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


// async function send(){
//   let response = await fetch('place-order/', {
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json',
//           'X-CSRFToken': getCookie('csrftoken') 
//       },
//       body: null
//   });
//   console.log(response)
//   if (response.ok){
//       let re = await response.json();
//       console.log(re)
//   }
// }




// const firebaseConfig = {
//   apiKey: "AIzaSyD1JVEEfALYm7AewLXIrWdY1dKognP5Mv8",
//   authDomain: "redlinegs-b0c63.firebaseapp.com",
//   projectId: "redlinegs-b0c63",
//   storageBucket: "redlinegs-b0c63.appspot.com",
//   messagingSenderId: "977169881582",
//   appId: "1:977169881582:web:10adfc014ae57f87e756ff",
//   measurementId: "G-M3E7Y3GH3C"
// };

// firebase.initializeApp(firebaseConfig);

// const messaging = firebase.messaging();

// messaging.onTokenRefresh(() => {
//   messaging.getToken()
//     .then(function (refreshedToken) {
//       console.log(refreshedToken);
//       showToken(refreshedToken);
//     }).catch((err) => {
//       console.log('Error al obtener el token actualziado:', err);
//       showToken('Unable to retrieve refreshed token ', err);
//     });
// })

//   messaging.onMessage(function (payload) {
//     console.log("Mensaje recibido en primer plano: ", payload);
//     registration.showNotification(payload.notification.title, {
//       body: payload.notification.body,
//       icon: '/firebase-logo.png'
//     });
//     appendMessage(payload);
//     // [END_EXCLUDE]

//   });


// // Registrar el Service Worker y solicitar permisos para notificaciones
// navigator.serviceWorker.register('firebase-messaging-sw.js').then((registration) => {
//   console.log("Service Worker registrado exitosamente:", registration);
//   messaging.onMessage((payload) => {
//     console.log("Mensaje recibido en primer plano:", payload);
//     // Usar el Service Worker para mostrar la notificación
//     registration.showNotification(payload.notification.title, {
//       body: payload.notification.body,
//       icon: '/firebase-logo.png'
//     });
//   });
//   return Notification.requestPermission();
// }).then(permission => {
//   if (permission !== 'granted') {
//     throw new Error("El usuario no concedió permisos de notificación.");
//   }
//   return getToken(messaging, {
//     vapidKey: 'BINXFXJWk3U5VbOvxRrqmv5HFVLDexKosPJ-Ze_-qrCFeyoxfVYXsFxIfONDG0H7dFx7u89BhJnARefTBn91eiw',
//     serviceWorkerRegistration: registration
//   });
// }).then(currentToken => {
//   if (!currentToken) {
//     throw new Error("Token no disponible");
//   }
//   console.log("Token de FCM:", currentToken);
//   return fetch('/api/save_token/', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ token: currentToken }),
//   });
// }).then(response => response.text())
//   .then(data => console.log("Respuesta del servidor:", data))
//   .catch(error => console.log("Error:", error));
