import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyBnMJW79RfIGGG6DvudKYzgsWlq6oY5Ofs",
  authDomain: "aswin-praveen-to-do-list.firebaseapp.com",
  projectId: "aswin-praveen-to-do-list",
  storageBucket: "aswin-praveen-to-do-list.firebasestorage.app",
  messagingSenderId: "97150751962",
  appId: "1:97150751962:web:03178b4865f8e2c68201e3",
  measurementId: "G-9MEHD6ZJGD"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Set up Google authentication
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider };
