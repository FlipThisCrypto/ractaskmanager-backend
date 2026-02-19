// Firebase config loaded from server endpoint (keeps keys out of git)
let firebaseConfig = {};

async function loadFirebaseConfig() {
  try {
    const response = await fetch("/api/firebase-config");
    firebaseConfig = await response.json();
  } catch (e) {
    console.error("Failed to load Firebase config:", e);
  }
  return firebaseConfig;
}

export { firebaseConfig, loadFirebaseConfig };
