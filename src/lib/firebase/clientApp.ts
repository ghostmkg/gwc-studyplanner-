
import { initializeApp, getApps, type FirebaseApp } from "firebase/app";
import { getAuth, type Auth } from "firebase/auth";
import { getFirestore, type Firestore } from "firebase/firestore";
import { getStorage, type Storage } from "firebase/storage";

// Your web app's Firebase configuration (as provided by user)
const firebaseConfig = {
  apiKey: "AIzaSyBsD_zoKqaBgzCILLdZCoXaY9oRJKL74q4",
  authDomain: "classcompanion-c1599.firebaseapp.com",
  projectId: "classcompanion-c1599",
  storageBucket: "classcompanion-c1599.firebasestorage.app", // Corrected: was .firebasestorage.app
  messagingSenderId: "51351055563",
  appId: "1:51351055563:web:da4ec8525e6791441ebf4e",
  measurementId: "G-ZRZ01DHR4J"
};

let app: FirebaseApp;
let auth: Auth;
let db: Firestore;
let storage: Storage;

if (typeof window !== 'undefined' && !getApps().length) {
  app = initializeApp(firebaseConfig);
  auth = getAuth(app);
  db = getFirestore(app);
  storage = getStorage(app);
} else if (getApps().length > 0) {
  app = getApps()[0];
  auth = getAuth(app);
  db = getFirestore(app);
  storage = getStorage(app);
}

// @ts-ignore
export { app, auth, db, storage };
