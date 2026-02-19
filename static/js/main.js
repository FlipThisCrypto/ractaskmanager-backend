import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js';
import { getAuth, onAuthStateChanged } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js';
import { getFirestore, collection, getDocs } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js';
import { firebaseConfig } from './firebase-config.js';

// Initialize Firebase
const firebaseConfig = await loadFirebaseConfig();
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Ensure user is authenticated
onAuthStateChanged(auth, (user) => {
    if (!user) {
        // If user is not authenticated, redirect to login
        window.location.href = '/login';
    }
});

// Function to fetch data from a Firestore collection
async function fetchData(collectionName) {
    try {
        const querySnapshot = await getDocs(collection(db, collectionName));
        const data = [];
        querySnapshot.forEach((doc) => {
            data.push({ id: doc.id, ...doc.data() });
        });
        console.log(`Fetched ${collectionName}:`, data);
        return data;
    } catch (error) {
        console.error(`Error fetching ${collectionName}:`, error);
        return [];
    }
}

// Functions to fetch specific collections
export async function fetchTasks() {
    return await fetchData('tasks');
}

export async function fetchMessages() {
    return await fetchData('messages');
}

export async function fetchChecklists() {
    return await fetchData('checklists');
}

export async function fetchLockerKeys() {
    return await fetchData('locker-keys');
}

export async function fetchChurchMeetings() {
    return await fetchData('church-meetings');
}

export async function fetchMoves() {
    return await fetchData('moves');
}

// Example: Call these functions when the page loads (for testing)
window.addEventListener('DOMContentLoaded', async () => {
    const path = window.location.pathname;
    if (path === '/tasks') {
        await fetchTasks();
    } else if (path === '/messages') {
        await fetchMessages();
    } else if (path === '/checklists') {
        await fetchChecklists();
    } else if (path === '/locker-keys') {
        await fetchLockerKeys();
    } else if (path === '/church-meetings') {
        await fetchChurchMeetings();
    } else if (path === '/moves') {
        await fetchMoves();
    }
});