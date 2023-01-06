importScripts("https://www.gstatic.com/firebasejs/8.2.1/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.2.1/firebase-messaging.js");

firebase.initializeApp ({
    apiKey: "AIzaSyCVDz_TkGY-Idf19AqAGIT6JcPLyICqhpY",
    authDomain: "deliverese-50037.firebaseapp.com",
    projectId: "deliverese-50037",
    storageBucket: "deliverese-50037.appspot.com",
    messagingSenderId: "567277528482",
    appId: "1:567277528482:web:efeeb054117440d18bfefb"
});

const messaging = firebase.messaging();
