const CACHE_NAME = 'rac-task-manager-cache-v1';
const urlsToCache = [
    '/static/style.css',
    '/static/app-icon.png',
    '/static/js/firebase-config.js',
    '/static/js/main.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js',
    'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js',
    'https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js'
];

// Install event: Cache static files
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Service Worker: Caching files');
                return cache.addAll(urlsToCache);
            })
    );
});

// Activate event: Clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.filter((name) => name !== CACHE_NAME)
                    .map((name) => caches.delete(name))
            );
        })
    );
});

// Fetch event: Serve cached files, bypass /login
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Bypass caching for /login route
    if (url.pathname === '/login') {
        event.respondWith(fetch(event.request));
        return;
    }

    // Cache-first strategy for other requests
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                return response || fetch(event.request).then((networkResponse) => {
                    // Cache the response for future use
                    if (networkResponse.ok) {
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, networkResponse.clone());
                        });
                    }
                    return networkResponse;
                });
            })
            .catch(() => {
                console.error('Service Worker: Fetch failed');
            })
    );
});